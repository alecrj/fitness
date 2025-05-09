# gunicorn_config.py
import multiprocessing
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Server socket
bind = os.getenv('GUNICORN_BIND', '0.0.0.0:5000')
backlog = 2048

# Worker processes
workers = int(os.getenv('GUNICORN_WORKERS', multiprocessing.cpu_count() * 2 + 1))
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2

# Server mechanics
daemon = False
user = None
group = None
umask = 0
tmp_upload_dir = None

# Logging
accesslog = '-'
errorlog = '-'
loglevel = 'info'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

# Process naming
proc_name = 'fitness-food-app'

# Application
wsgi_app = 'app:create_app()'

# Server hooks
def on_starting(server):
    """
    Called just before the master process is initialized.
    """
    pass

def on_exit(server):
    """
    Called just before exiting.
    """
    pass

def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    """
    server.log.info("Worker spawned (pid: %s)", worker.pid)

def pre_fork(server, worker):
    """
    Called just prior to forking a new worker.
    """
    pass

def pre_request(worker, req):
    """
    Called just before a worker processes the request.
    """
    worker.log.debug("%s %s", req.method, req.path)

def post_request(worker, req, environ, resp):
    """
    Called after a worker processes the request.
    """
    pass