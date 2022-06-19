import multiprocessing

name = "Gunicorn config for FastAPI - TutLinks.com"

accesslog = "/app/gunicorn-access.log"
errorlog = "/app/gunicorn-error.log"

bind = "0.0.0.0:8000"

worker_class = "uvicorn.workers.UvicornWorker"
workers = multiprocessing.cpu_count() * 2 + 1
worker_connections = 1024
backlog = 2048
max_requests = 5120
timeout = 120
keepalive = 2

reload = True
preload_app = False
daemon = False
