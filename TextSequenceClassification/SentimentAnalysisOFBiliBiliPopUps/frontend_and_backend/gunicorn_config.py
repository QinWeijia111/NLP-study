# gunicorn_config.py
bind = "36.103.203.203:27852"  # 绑定地址和端口
workers = 4  # 工作进程数，根据 CPU 核心数调整
worker_class = "sync"  # 工作模式，常用 'sync' 或 'gevent'
timeout = 30  # 超时时间，单位为秒
loglevel = "info"  # 日志级别
errorlog = "-"  # 错误日志，'-' 表示输出到标准输出
accesslog = "-"  # 访问日志，'-' 表示输出到标准输出
