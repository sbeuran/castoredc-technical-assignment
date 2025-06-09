import multiprocessing

# Gunicorn config variables
bind = "0.0.0.0:8000"
workers = multiprocessing.cpu_count() * 2 + 1
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 600
chdir = "/home/site/wwwroot"
wsgi_app = "app.main:app"
accesslog = "-"
errorlog = "-"
loglevel = "info"
capture_output = True 