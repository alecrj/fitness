"""Health check utilities for monitoring application status"""
import time
import os
import logging
from typing import Dict, Any
import firebase_admin
from flask import current_app
import requests

# Configure logging
logger = logging.getLogger('health_check')

def check_firebase_connection():
    """Check Firebase connection
    
    Returns:
        Dict with connection status and latency
    """
    try:
        # Get Firestore client
        db = firebase_admin.firestore.client()
        
        # Measure latency
        start_time = time.time()
        
        # Simple operation to verify connection
        db.collection('health_checks').document('status').get()
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        return {
            'status': 'connected',
            'latency_ms': round(latency_ms, 2)
        }
    except Exception as e:
        logger.error(f"Firebase health check failed: {str(e)}")
        
        return {
            'status': 'error',
            'error': str(e)
        }

def check_usda_api():
    """Check USDA API connection
    
    Returns:
        Dict with connection status and latency
    """
    try:
        # Get API key from config
        api_key = current_app.config.get('USDA_API_KEY')
        if not api_key:
            return {'status': 'not_configured'}
            
        # Measure latency
        start_time = time.time()
        
        # Make a simple API request
        url = current_app.config.get('USDA_API_BASE_URL') + '/foods/search'
        response = requests.get(
            url,
            params={
                'api_key': api_key,
                'query': 'apple',
                'pageSize': 1
            },
            timeout=5
        )
        
        # Calculate latency
        latency_ms = (time.time() - start_time) * 1000
        
        if response.status_code == 200:
            return {
                'status': 'connected',
                'latency_ms': round(latency_ms, 2)
            }
        else:
            return {
                'status': 'error',
                'http_status': response.status_code,
                'error': response.text[:100]  # First 100 chars of error
            }
    except requests.exceptions.RequestException as e:
        logger.error(f"USDA API health check failed: {str(e)}")
        
        return {
            'status': 'error',
            'error': str(e)
        }

def check_system_resources():
    """Check system resources
    
    Returns:
        Dict with system resource information
    """
    try:
        import psutil
    except ImportError:
        return {'status': 'psutil_not_installed'}
        
    try:
        # Get CPU usage
        cpu_percent = psutil.cpu_percent(interval=0.1)
        
        # Get memory usage
        memory = psutil.virtual_memory()
        memory_used_mb = memory.used / (1024 * 1024)
        memory_total_mb = memory.total / (1024 * 1024)
        memory_percent = memory.percent
        
        # Get disk usage
        disk = psutil.disk_usage('/')
        disk_used_gb = disk.used / (1024 * 1024 * 1024)
        disk_total_gb = disk.total / (1024 * 1024 * 1024)
        disk_percent = disk.percent
        
        return {
            'status': 'ok',
            'cpu': {
                'percent': round(cpu_percent, 1)
            },
            'memory': {
                'used_mb': round(memory_used_mb, 1),
                'total_mb': round(memory_total_mb, 1),
                'percent': round(memory_percent, 1)
            },
            'disk': {
                'used_gb': round(disk_used_gb, 1),
                'total_gb': round(disk_total_gb, 1),
                'percent': round(disk_percent, 1)
            }
        }
    except Exception as e:
        logger.error(f"System resources check failed: {str(e)}")
        
        return {
            'status': 'error',
            'error': str(e)
        }

def get_application_info():
    """Get application information
    
    Returns:
        Dict with application information
    """
    # Get environment
    env = os.environ.get('FLASK_ENV', 'development')
    
    # Get version or build info (if available)
    version = os.environ.get('APP_VERSION', '1.0.0')
    
    # Get uptime
    uptime_seconds = time.time() - current_app.get('start_time', time.time())
    
    # Format uptime
    days, remainder = divmod(uptime_seconds, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    uptime_str = ''
    if days > 0:
        uptime_str += f"{int(days)}d "
    if hours > 0 or days > 0:
        uptime_str += f"{int(hours)}h "
    if minutes > 0 or hours > 0 or days > 0:
        uptime_str += f"{int(minutes)}m "
    uptime_str += f"{int(seconds)}s"
    
    return {
        'environment': env,
        'version': version,
        'uptime_seconds': int(uptime_seconds),
        'uptime': uptime_str
    }

def check_health() -> Dict[str, Any]:
    """Comprehensive health check
    
    Returns:
        Dict with health check results
    """
    # Measure total check time
    start_time = time.time()
    
    # Run all checks
    health_data = {
        'timestamp': time.time(),
        'status': 'healthy',  # Default to healthy, will be updated if any checks fail
        'application': get_application_info(),
        'dependencies': {
            'firebase': check_firebase_connection(),
            'usda_api': check_usda_api()
        }
    }
    
    # Add system resources if enabled
    if os.environ.get('ENABLE_SYSTEM_METRICS', 'False').lower() == 'true':
        health_data['system'] = check_system_resources()
    
    # Check overall status
    for dep_name, dep_status in health_data['dependencies'].items():
        if dep_status.get('status') != 'connected':
            # If a critical dependency is down, mark as unhealthy
            if dep_name in ['firebase']:
                health_data['status'] = 'unhealthy'
            # If a non-critical dependency is down, mark as degraded
            else:
                health_data['status'] = 'degraded'
    
    # Add check duration
    health_data['check_duration_ms'] = round((time.time() - start_time) * 1000, 2)
    
    return health_data