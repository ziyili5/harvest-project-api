# gunicorn configuration file
import pathlib

pathlib.Path("logs").mkdir(exist_ok=True)

bind = "0.0.0.0:3000"
workers = 2

# Logging
loglevel = "debug"
errorlog = "logs/gunicorn_error.log"
accesslog = "logs/gunicorn_access.log"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s"'
