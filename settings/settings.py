# coding: utf-8

import socket
import os
import environ

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DEBUG = True

# 获取本机IP
IP = socket.getaddrinfo(socket.gethostname(), None)[-1][4][0]

# 读取配置文件
env = environ.Env()
env_file = "config/%s.env" % ('pro' if IP == '172.20.3.150' else 'local')
env_path = os.path.join(BASE_DIR, env_file)
print("load env %s" % env_path)
env.read_env(env_path)

# 数据库配置
DB_HOST = env.str('DB_HOST')
DB_PORT = env.int('DB_PORT')
DB_USER = env.str('DB_USER')
DB_PASSWORD = env.str('DB_PASSWORD')
DB_NAME = env.str('DB_NAME')
TS_TOKEN = env.str('TS_TOKEN')
