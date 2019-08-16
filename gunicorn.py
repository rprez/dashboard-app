"""gunicorn WSGI server configuration."""
from multiprocessing import cpu_count

def max_workers():
    return cpu_count()

bind = '0.0.0.0:8000'
backlog = 2048
workers = max_workers()
worker_class = 'sync'
worker_connections = 1000
timeout = 30
keepalive = 2
proc_name = None
errorlog = 'logs/gunicorn.log'
loglevel = 'info'
accesslog = '-'
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'

def on_starting(server):
    """
    Called just before the master process is initialized.
    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass

def on_reload(server):
    """
    Called to recycle workers during a reload via SIGHUP.
    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass

def when_ready(server):
    """
    Called just after the server is started.
    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass

def pre_fork(server, worker):
    """
    Called just before a worker is forked.
    The callable needs to accept two instance variables for the Arbiter and
    new Worker.
    """
    pass

def post_fork(server, worker):
    """
    Called just after a worker has been forked.
    The callable needs to accept two instance variables for the Arbiter and
    new Worker.
    """
    pass

def post_worker_init(worker):
    """
    Called just after a worker has initialized the application.
    The callable needs to accept one instance variable for the initialized
    Worker.
    """
    pass

def worker_init(worker):
    """
    Called just after a worker exited on SIGINT or SIGQUIT.
    The callable needs to accept one instance variable for the initialized
    Worker.
    """
    pass

def worker_abort(worker):
    """
    Called when a worker received the SIGABRT signal.
    This call generally happens on timeout.
    The callable needs to accept one instance variable for the initialized
    Worker.
    """
    pass

def pre_exec(server):
    """
    Called just before a new master process is forked.
    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass

def pre_request(worker, req):
    """
    Called just before a worker processes the request.
    The callable needs to accept two instance variables for the Worker and
    the Request.
    """
    worker.log.debug("%s %s" % (req.method, req.path))

def post_request(worker, req, environ, resp):
    """
    Called after a worker processes the request.
    The callable needs to accept two instance variables for the Worker and
    the Request.
    """
    pass

def worker_exit(server, worker):
    """
    Called just after a worker has been exited.
    The callable needs to accept two instance variables for the Arbiter and
    the just-exited Worker.
    """
    pass

def nworkers_changed(server, new_value, old_value):
    """
    Called just after num_workers has been changed.
    The callable needs to accept an instance variable of the Arbiter and two
    integers of number of workers after and before change.
    If the number of workers is set for the first time, old_value would be
    None.
    """
    pass

def on_exit(server):
    """
    Called just before exiting gunicorn.
    The callable needs to accept a single instance variable for the Arbiter.
    """
    pass