"""
@auth: cyq
@name: errors
@desc: 权限与错误处理
"""
import json
from functools import wraps

from flask import g, jsonify, make_response
from Model.Models import User
from . import v1
from .. import auth


@v1.after_request
def after_request(response):
    return response


@v1.app_errorhandler(404)
def page_not_found(e):
    return jsonify(dict(err="请求的数据找不着,再康康")),404

@v1.app_errorhandler(500)
def host_err(e):
    return jsonify(dict(err="服务器有点问题,再康康")),500
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


def is_admin(func):
    """判断登录用户是否是admin"""
    @wraps(func)
    def wrap_func(*args, **kwargs):
        try:
            if not g.user.is_superuser():
                return make_response(
                    jsonify({"code":1,'err': '没权限啊铁汁'}), 403)
            return func(*args, **kwargs)
        except KeyError:
            return make_response(
                jsonify({"code": 1, 'err': '没权限啊铁汁'}), 403)

    return wrap_func




class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv



@v1.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response
