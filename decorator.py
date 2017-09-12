#encoding:utf-8
from functools import wraps
from flask import session,redirect,url_for

def login_restriction(func):
    #@wraps(func)的作用是保持func的函数名不变，不会被改成wrapper
    #*args,**kwargs可以组合起来表示任何参数
    @wraps(func)
    def wrapper(*args,**kwargs):
        if session.get('user_id'):
            return func(*args,**kwargs)
        else:
            return redirect(url_for('index'))
    return wrapper