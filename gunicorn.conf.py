# gunicorn.conf.py
bind = "0.0.0.0:10000"
workers = 1  # Use only 1 worker to conserve memory
worker_class = "sync"
timeout = 120  # Increase timeout to 2 minutes
keepalive = 5
max_requests = 100
max_requests_jitter = 10
preload_app = True  # Load the app before forking workers
