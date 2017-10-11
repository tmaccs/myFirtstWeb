#encoding:utf-8
import os
from datetime import timedelta
DEBUG=True

#SECRET_KEY=os.urandom(24),这样session会一直出问题
SECRET_KEY='yanghengyu'
#单词写错了！PERMANENT_SESSION_LIFTIME=timedelta(days=7)
PERMANENT_SESSION_LIFETIME=timedelta(days=7)



#dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
USERNAME = 'root'
PASSWORD = 'root'
HOST = '127.0.0.1'
PORT = '3306'
DATABASE = 'try_demo2'

#SQLALchemy会在config中来找名为SQLALCHEMY_DATABASE_URI的字符串，读取其中的配置
SQLALCHEMY_DATABASE_URI='{}+{}://{}:{}@{}:{}/{}?charset=utf8'.format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False
