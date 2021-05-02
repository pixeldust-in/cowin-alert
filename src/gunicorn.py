# -*- coding: utf-8 -*-
import multiprocessing
import os

DEFAULT_NUM_WORKERS = multiprocessing.cpu_count() * 2 + 1

bind = f"unix:/tmp/{os.getenv('APP')}.sock"
workers = os.getenv("NUM_WORKERS", default=DEFAULT_NUM_WORKERS)
accesslog = "-"
access_log_format = '%(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" in %(D)sµs'
log_level = os.getenv("LOG_LEVEL", default="INFO")
timeout = 3600
capture_output = True
enable_stdio_inheritance = True
max_requests = 1000
max_requests_jitter = 50
