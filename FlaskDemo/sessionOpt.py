# encoding: utf-8
"""
@auth: cyq
@name: sessionOpt
@desc: session 简单实现
"""

from FlaskDemo import app
from flask import session,request

@app.route('/')
def home():
    if not session.get("user"):
        return "没有登录"
    return "你好"


@app.route('/login')
def login():
    username = request.args.get("username")
    password = request.args.get("password")
    if username and password:
        session['user'] = username + password
        return "ok"
    return "err"


@app.route("/logout")
def logout():
    session.pop("user", None)
    return "ok"
