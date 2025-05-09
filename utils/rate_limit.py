"""Rate limiting utilities for API protection"""
import time
from functools import wraps
from flask import request, jsonify, current_app
import redis
import hashlib

# Optional Redis connection - can be configured in production
redis_client = None

def get_redis_client():
    """Get or create Redis client for rate limiting"""
    global redis_client
    if redis_client is None:
        try:
            # Try to initialize Redis if configured
            redis_url = current_app.config.get('REDIS_URL')
            if redis_url:
                redis_client = redis.from_url(redis_url)
            else:
                # Fall back to in-memory rate limiting
                return None
        except (redis.exceptions.ConnectionError, ImportError):
            # Fall back to in-memory rate limiting
            return None
    return redis_client

# Fallback in-memory rate limiting when Redis is not available
class InMemoryRateLimiter:
    """Simple in-memory rate limiter for development or small deployments"""
    
    def __init__(self):
        self.rate_limits = {}
        
    def check_rate_limit(self, key, limit, period):
        """Check if a key is rate limited
        
        Args:
            key: Unique identifier for the client
            limit: Maximum number of requests allowed in the period
            period: Time period in seconds
            
        Returns:
            Tuple of (is_allowed, remaining, reset_time)
        """
        current_time = time.time()
        
        # Clean up expired entries
        self._cleanup()
        
        # Get/create record for this key
        if key not in self.rate_limits:
            self.rate_limits[key] = {
                'count': 0,
                'reset_at': current_time + period
            }
            
        record = self.rate_limits[key]
        
        # Reset if period has expired
        if current_time > record['reset_at']:
            record['count'] = 0
            record['reset_at'] = current_time + period
            
        # Check limit
        is_allowed = record['count'] < limit
        
        # Increment counter if allowed
        if is_allowed:
            record['count'] += 1
            
        remaining = max(0, limit - record['count'])
        reset_time = record['reset_at']
        
        return is_allowed, remaining, reset_time
        
    def _cleanup(self):
        """Remove expired rate limit records"""
        current_time = time.time()
        # Use a list to avoid modifying dictionary during iteration
        expired_keys = [k for k, v in self.rate_limits.items() if current_time > v['reset_at']]
        for key in expired_keys:
            del self.rate_limits[key]

# Singleton in-memory rate limiter
memory_rate_limiter = InMemoryRateLimiter()

def check_rate_limit(key, limit, period):
    """Check if a request is within rate limits
    
    Args:
        key: Unique identifier for the client
        limit: Maximum number of requests allowed in the period
        period: Time period in seconds
        
    Returns:
        Tuple of (is_allowed, remaining, reset_time)
    """
    redis_client = get_redis_client()
    
    if redis_client:
        # Use Redis-based rate limiting
        redis_key = f"rate_limit:{key}"
        count = redis_client.incr(redis_key)
        
        # Set expiry if this is the first request in the period
        if count == 1:
            redis_client.expire(redis_key, period)
            
        # Check if request is within the limit
        ttl = redis_client.ttl(redis_key)
        reset_time = time.time() + ttl
        is_allowed = count <= limit
        remaining = max(0, limit - count)
        
        return is_allowed, remaining, reset_time
    else:
        # Fall back to in-memory rate limiting
        return memory_rate_limiter.check_rate_limit(key, limit, period)

def get_request_identifier():
    """Generate a unique identifier for the current request
    
    Uses a combination of IP address and user ID if available
    
    Returns:
        String identifier
    """
    # Get client IP
    ip = request.remote_addr
    
    # Get user ID if authenticated
    from utils.firebase_admin import get_current_user
    user = get_current_user()
    user_id = user['uid'] if user else 'anonymous'
    
    # Create combined key
    key = f"{ip}:{user_id}"
    
    # Hash the key for privacy
    return hashlib.md5(key.encode()).hexdigest()

def rate_limit(limit=100, period=60, by_endpoint=True):
    """Decorator to apply rate limiting to API endpoints
    
    Args:
        limit: Maximum number of requests allowed in the period
        period: Time period in seconds
        by_endpoint: Whether to apply rate limit per endpoint (True) or globally (False)
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # Generate rate limit key
            base_key = get_request_identifier()
            if by_endpoint:
                endpoint = request.endpoint
                key = f"{base_key}:{endpoint}"
            else:
                key = base_key
                
            # Check rate limit
            is_allowed, remaining, reset_time = check_rate_limit(key, limit, period)
            
            # Set rate limit headers
            response_headers = {
                'X-RateLimit-Limit': str(limit),
                'X-RateLimit-Remaining': str(remaining),
                'X-RateLimit-Reset': str(int(reset_time))
            }
            
            if not is_allowed:
                # Rate limit exceeded
                response = jsonify({
                    'error': 'Rate limit exceeded',
                    'message': f'Too many requests. Please try again after {int(reset_time - time.time())} seconds.'
                })
                response.status_code = 429
                
                # Add headers to response
                for key, value in response_headers.items():
                    response.headers[key] = value
                    
                return response
                
            # Continue with the original request
            response = f(*args, **kwargs)
            
            # Add rate limit headers to the response
            if hasattr(response, 'headers'):
                for key, value in response_headers.items():
                    response.headers[key] = value
                    
            return response
        return decorated_function
    return decorator

# Route-specific rate limits
def auth_rate_limit():
    """Specific rate limit for authentication endpoints"""
    return rate_limit(limit=20, period=60, by_endpoint=True)

def standard_rate_limit():
    """Standard rate limit for most API endpoints"""
    return rate_limit(limit=60, period=60, by_endpoint=True)

def search_rate_limit():
    """Rate limit for search endpoints"""
    return rate_limit(limit=10, period=10, by_endpoint=True)