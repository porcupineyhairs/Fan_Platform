"""
@auth: cyq
@name: errors
@desc: 错误处理
"""
import json

from flask import g, jsonify
from Model.Models import User
from . import v1
from .. import auth



# @v1.app_errorhandler(HTTPException)
# def errHandler(e):
#     res = e.get_response()
#     res.data = json.dumps({
#         "code":e.code,
#         "name":e.name,
#         "desc":e.description
#     })
#     res.content_type = "application/json"
#     return res
#     # return jsonify(dict(err="请求的方法有点问题,再康康")),405

@v1.app_errorhandler(404)
def page_not_found(e):
    return jsonify(dict(err="请求的地址有点问题,再康康")),404

@v1.app_errorhandler(500)
def host_err(e):
    return jsonify(dict(err="请求的地址有点问题,再康康")),500
@v1.app_errorhandler(403)
def host_err(e):
    return jsonify(dict(err="有问题啊,再康康吧")),500


@auth.error_handler
def unauthorized():
    return jsonify(dict(err="请求没有权限啊,在康康")), 401


@auth.verify_password
def verify_password_or_token(username_or_token, password):
    user = User.verify_token(token=username_or_token)
    if not user:
        user = User.query.filter(User.username == username_or_token).first()
        if not user or not user.verify_password(password):
            return False
    g.user = user
    return True
