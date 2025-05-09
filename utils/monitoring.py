"""Performance monitoring utilities for the application"""
import time
import functools
import logging
import threading
from flask import request, g
from typing import Dict, Any, List, Optional

# Configure logging
logger = logging.getLogger('monitoring')

# Metrics storage
class Metrics:
    """Simple metrics collector"""
    def __init__(self):
        self.metrics = {}
        self.lock = threading.Lock()
        
    def record(self, name: str, value: float, tags: Optional[Dict[str, str]] = None):
        """Record a metric value
        
        Args:
            name: Metric name
            value: Metric value
            tags: Optional tags to categorize the metric
        """
        tags = tags or {}
        
        # Create key for this combination of name and tags
        tag_key = ','.join(f"{k}:{v}" for k, v in sorted(tags.items()))
        key = f"{name}:{tag_key}" if tag_key else name
        
        with self.lock:
            if key not in self.metrics:
                self.metrics[key] = {
                    'name': name,
                    'tags': tags,
                    'count': 0,
                    'sum': 0,
                    'min': float('inf'),
                    'max': float('-inf'),
                    'values': []
                }
                
            metric = self.metrics[key]
            metric['count'] += 1
            metric['sum'] += value
            metric['min'] = min(metric['min'], value)
            metric['max'] = max(metric['max'], value)
            
            # Keep last 100 values for calculating percentiles
            metric['values'].append(value)
            if len(metric['values']) > 100:
                metric['values'].pop(0)
                
    def get_metrics(self) -> List[Dict[str, Any]]:
        """Get all collected metrics
        
        Returns:
            List of metric dictionaries
        """
        result = []
        
        with self.lock:
            for key, metric in self.metrics.items():
                # Calculate stats
                avg = metric['sum'] / metric['count'] if metric['count'] > 0 else 0
                
                # Calculate percentiles if we have values
                p50, p95, p99 = 0, 0, 0
                if metric['values']:
                    sorted_values = sorted(metric['values'])
                    p50 = sorted_values[int(len(sorted_values) * 0.5)]
                    p95 = sorted_values[int(len(sorted_values) * 0.95)]
                    p99 = sorted_values[int(len(sorted_values) * 0.99)]
                    
                result.append({
                    'name': metric['name'],
                    'tags': metric['tags'],
                    'count': metric['count'],
                    'sum': metric['sum'],
                    'avg': avg,
                    'min': metric['min'],
                    'max': metric['max'],
                    'p50': p50,
                    'p95': p95,
                    'p99': p99
                })
                
        return result
        
    def reset(self):
        """Reset all metrics"""
        with self.lock:
            self.metrics = {}

# Singleton metrics instance
metrics = Metrics()

def timing(name: str = None, tags: Optional[Dict[str, str]] = None):
    """Decorator to measure function execution time
    
    Args:
        name: Metric name (defaults to function name)
        tags: Optional tags to categorize the metric
        
    Returns:
        Decorated function
    """
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            # Start timer
            start_time = time.time()
            
            # Determine metric name
            metric_name = name or f.__name__
            
            try:
                # Execute the function
                result = f(*args, **kwargs)
                
                # Record execution time
                duration_ms = (time.time() - start_time) * 1000
                metrics.record(f"{metric_name}.time_ms", duration_ms, tags)
                
                return result
            except Exception as e:
                # Record error
                metric_tags = dict(tags or {})
                metric_tags['error'] = str(e).split(':')[0]  # Use only error type for tag
                metrics.record(f"{metric_name}.error", 1, metric_tags)
                
                # Re-raise the exception
                raise
                
        return decorated_function
    return decorator

def track_api_performance():
    """Middleware to track API request performance"""
    # Get request start time
    start_time = g.get('request_start_time')
    if not start_time:
        return
        
    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000
    
    # Create tags
    tags = {
        'method': request.method,
        'endpoint': request.endpoint or 'unknown',
        'status': str(request.environ.get('REMOTE_ADDR', 'unknown')),
    }
    
    # Record metrics
    metrics.record('api.response_time_ms', duration_ms, tags)
    metrics.record('api.request', 1, tags)

def track_external_api_call(name, start_time, success=True, additional_tags=None):
    """Track performance of external API calls
    
    Args:
        name: API name
        start_time: Start time of the API call
        success: Whether the call was successful
        additional_tags: Additional tags for the metric
    """
    # Calculate duration
    duration_ms = (time.time() - start_time) * 1000
    
    # Create tags
    tags = additional_tags or {}
    tags['success'] = 'true' if success else 'false'
    
    # Record metrics
    metrics.record(f'external_api.{name}.time_ms', duration_ms, tags)
    metrics.record(f'external_api.{name}.call', 1, tags)

def get_performance_stats():
    """Get performance statistics for monitoring
    
    Returns:
        Dictionary with performance metrics
    """
    return {
        'metrics': metrics.get_metrics()
    }