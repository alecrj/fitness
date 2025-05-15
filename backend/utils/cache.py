"""Simple caching utility for improving performance"""
import time
import functools
import json
import hashlib
from flask import current_app

# Simple in-memory cache
class SimpleCache:
    """Simple in-memory cache implementation"""
    
    def __init__(self):
        self.cache = {}
        
    def get(self, key):
        """Get a value from the cache
        
        Args:
            key: Cache key
            
        Returns:
            Cached value or None if not found or expired
        """
        if key not in self.cache:
            return None
            
        item = self.cache[key]
        
        # Check if expired
        if item['expires_at'] and time.time() > item['expires_at']:
            # Remove expired item
            del self.cache[key]
            return None
            
        return item['value']
        
    def set(self, key, value, timeout=None):
        """Set a value in the cache
        
        Args:
            key: Cache key
            value: Value to cache
            timeout: Cache timeout in seconds (None for no expiration)
        """
        expires_at = time.time() + timeout if timeout else None
        
        self.cache[key] = {
            'value': value,
            'expires_at': expires_at
        }
        
    def delete(self, key):
        """Delete a value from the cache
        
        Args:
            key: Cache key
        """
        if key in self.cache:
            del self.cache[key]
            
    def clear(self):
        """Clear all values from the cache"""
        self.cache.clear()

# Create singleton cache instance
cache = SimpleCache()

def cached(timeout=None, key_prefix=''):
    """Decorator to cache function results
    
    Args:
        timeout: Cache timeout in seconds (defaults to DEFAULT_CACHE_TIMEOUT config)
        key_prefix: Prefix for cache key
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Get timeout from config if not specified
            if timeout is None:
                cache_timeout = current_app.config.get('DEFAULT_CACHE_TIMEOUT', 300)
            else:
                cache_timeout = timeout
                
            # Skip caching if timeout is 0
            if cache_timeout == 0:
                return f(*args, **kwargs)
                
            # Generate cache key
            cache_key = _make_cache_key(f, key_prefix, args, kwargs)
            
            # Try to get from cache
            value = cache.get(cache_key)
            if value is not None:
                return value
                
            # Call the function and cache the result
            value = f(*args, **kwargs)
            cache.set(cache_key, value, timeout=cache_timeout)
            
            return value
        return decorated_function
    return decorator

def invalidate(key_prefix):
    """Decorator to invalidate cache entries
    
    Args:
        key_prefix: Prefix of cache keys to invalidate
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Call the function
            result = f(*args, **kwargs)
            
            # Invalidate cache entries with the given prefix
            keys_to_delete = []
            for key in cache.cache.keys():
                if key.startswith(key_prefix):
                    keys_to_delete.append(key)
                    
            for key in keys_to_delete:
                cache.delete(key)
                
            return result
        return decorated_function
    return decorator

def _make_cache_key(f, key_prefix, args, kwargs):
    """Generate a cache key for a function call
    
    Args:
        f: Function being called
        key_prefix: Prefix for the cache key
        args: Positional arguments
        kwargs: Keyword arguments
        
    Returns:
        Cache key string
    """
    # Start with prefix and function name
    key_parts = [key_prefix, f.__module__, f.__name__]
    
    # Add stringified args and kwargs
    for arg in args:
        key_parts.append(str(arg))
        
    for k, v in sorted(kwargs.items()):
        key_parts.append(f"{k}:{v}")
        
    # Join with colons
    key = ':'.join(key_parts)
    
    # Hash if the key is too long
    if len(key) > 250:
        key = hashlib.md5(key.encode()).hexdigest()
        
    return key