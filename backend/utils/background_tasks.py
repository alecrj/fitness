"""Background task processing system for handling long-running operations"""
import threading
import queue
import time
import traceback
import uuid
import json
import logging
from typing import Dict, Any, Callable
import firebase_admin
from firebase_admin import firestore

# Configure logging
logger = logging.getLogger('background_tasks')

# Task queue
task_queue = queue.Queue()

# Task registry
TASK_HANDLERS = {}

# Task status tracking
task_status = {}

def register_task(name: str):
    """Decorator to register a task handler
    
    Args:
        name: Name of the task
        
    Returns:
        Decorated function
    """
    def decorator(f):
        TASK_HANDLERS[name] = f
        return f
    return decorator

def enqueue_task(task_name: str, data: Dict[str, Any] = None, user_id: str = None) -> str:
    """Add a task to the background processing queue
    
    Args:
        task_name: Name of the task to run
        data: Task data/parameters
        user_id: ID of the user who initiated the task
        
    Returns:
        Task ID for tracking status
    """
    # Generate unique task ID
    task_id = str(uuid.uuid4())
    
    # Create task object
    task = {
        'id': task_id,
        'name': task_name,
        'data': data or {},
        'user_id': user_id,
        'created_at': time.time()
    }
    
    # Add to queue
    task_queue.put(task)
    
    # Initialize status
    task_status[task_id] = {
        'id': task_id,
        'name': task_name,
        'status': 'queued',
        'progress': 0,
        'created_at': task['created_at'],
        'started_at': None,
        'completed_at': None,
        'result': None,
        'error': None
    }
    
    # Log new task
    logger.info(f"Task enqueued: {task_name} (ID: {task_id})")
    
    # Store in Firestore if available
    try:
        db = firebase_admin.firestore.client()
        db.collection('tasks').document(task_id).set({
            **task_status[task_id],
            'created_at': firestore.SERVER_TIMESTAMP
        })
    except Exception as e:
        logger.error(f"Failed to store task in Firestore: {str(e)}")
    
    return task_id

def get_task_status(task_id: str) -> Dict[str, Any]:
    """Get the status of a background task
    
    Args:
        task_id: ID of the task
        
    Returns:
        Task status dictionary or None if not found
    """
    # Try in-memory status first
    if task_id in task_status:
        return task_status[task_id]
        
    # Fall back to Firestore
    try:
        db = firebase_admin.firestore.client()
        task_doc = db.collection('tasks').document(task_id).get()
        
        if task_doc.exists:
            return task_doc.to_dict()
    except Exception as e:
        logger.error(f"Failed to get task status from Firestore: {str(e)}")
        
    return None

def update_task_status(task_id: str, status: str = None, progress: int = None, 
                      result: Any = None, error: str = None):
    """Update the status of a background task
    
    Args:
        task_id: ID of the task
        status: New status (queued, running, completed, failed)
        progress: Progress percentage (0-100)
        result: Task result data
        error: Error message if failed
    """
    if task_id not in task_status:
        return
        
    task = task_status[task_id]
    
    # Update fields
    if status:
        task['status'] = status
        
    if progress is not None:
        task['progress'] = max(0, min(100, progress))
        
    if result is not None:
        # Ensure result is JSON serializable
        try:
            json.dumps(result)
            task['result'] = result
        except (TypeError, ValueError):
            task['result'] = str(result)
            
    if error:
        task['error'] = error
        
    # Set timestamps
    if status == 'running' and not task['started_at']:
        task['started_at'] = time.time()
        
    if status in ('completed', 'failed') and not task['completed_at']:
        task['completed_at'] = time.time()
        
    # Update in Firestore if available
    try:
        db = firebase_admin.firestore.client()
        
        # Convert timestamps for Firestore
        firestore_update = task.copy()
        if firestore_update.get('started_at'):
            firestore_update['started_at'] = firestore.SERVER_TIMESTAMP if status == 'running' else \
                                             firestore.Timestamp.from_seconds(int(task['started_at']))
                                             
        if firestore_update.get('completed_at'):
            firestore_update['completed_at'] = firestore.SERVER_TIMESTAMP if status in ('completed', 'failed') else \
                                               firestore.Timestamp.from_seconds(int(task['completed_at']))
                                               
        # Update document
        db.collection('tasks').document(task_id).update(firestore_update)
    except Exception as e:
        logger.error(f"Failed to update task status in Firestore: {str(e)}")

def process_task(task: Dict[str, Any]):
    """Process a single background task
    
    Args:
        task: Task to process
    """
    task_id = task['id']
    task_name = task['name']
    
    # Log task start
    logger.info(f"Processing task: {task_name} (ID: {task_id})")
    
    # Update status to running
    update_task_status(task_id, status='running', progress=0)
    
    try:
        # Check if handler exists
        if task_name not in TASK_HANDLERS:
            raise ValueError(f"Unknown task type: {task_name}")
            
        # Get handler
        handler = TASK_HANDLERS[task_name]
        
        # Create progress callback
        def progress_callback(percent):
            update_task_status(task_id, progress=percent)
            
        # Execute handler
        result = handler(task['data'], progress_callback)
        
        # Update status to completed
        update_task_status(task_id, status='completed', progress=100, result=result)
        
        # Log completion
        logger.info(f"Task completed: {task_name} (ID: {task_id})")
        
    except Exception as e:
        # Log error
        logger.error(f"Task failed: {task_name} (ID: {task_id}): {str(e)}")
        logger.error(traceback.format_exc())
        
        # Update status to failed
        update_task_status(
            task_id, 
            status='failed', 
            error=f"{str(e)}\n{traceback.format_exc()}"
        )

def task_worker():
    """Background worker that processes tasks from the queue"""
    logger.info("Background task worker started")
    
    while True:
        try:
            # Get next task from queue
            task = task_queue.get(block=True, timeout=1.0)
            
            # Process the task
            process_task(task)
            
            # Mark task as done
            task_queue.task_done()
            
        except queue.Empty:
            # No tasks in queue
            pass
        except Exception as e:
            # Log unexpected errors
            logger.error(f"Error in task worker: {str(e)}")
            logger.error(traceback.format_exc())

def start_background_workers(num_workers=1):
    """Start background task processing workers
    
    Args:
        num_workers: Number of worker threads to start
    """
    for i in range(num_workers):
        worker = threading.Thread(target=task_worker, daemon=True)
        worker.start()
        logger.info(f"Started background worker {i+1}")

# Example task handler
@register_task('example_task')
def handle_example_task(data, progress_callback):
    """Example task handler for testing
    
    Args:
        data: Task data/parameters
        progress_callback: Function to report progress percentage
        
    Returns:
        Task result
    """
    # Simulate work
    total_steps = data.get('steps', 10)
    
    for i in range(total_steps):
        # Do some work
        time.sleep(0.5)
        
        # Report progress
        progress = int((i + 1) / total_steps * 100)
        progress_callback(progress)
        
    # Return result
    return {
        'message': 'Example task completed successfully',
        'processed_items': total_steps
    }

# Initialize workers when imported
start_background_workers(num_workers=2)