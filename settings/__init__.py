# coding: utf-8
import os

TOKEN = os.environ.get('TOKEN', '')
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_PORT = int(os.environ.get('DB_PORT', 3306))
DB_PASSWD = os.environ.get('DB_PASSWD', '')
DB_USER = os.environ.get('DB_USER', '')
DB_NAME = os.environ.get('DB_NAME', '')

# 发件邮箱配置
MAIL_USER = os.environ.get('MAIL_USER', '')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD', '')
MAIL_SMTP_SERVER = os.environ.get('MAIL_SMTP_SERVER', '')
MAIL_RECIEVERS = os.environ.get('MAIL_RECIEVERS', '')
