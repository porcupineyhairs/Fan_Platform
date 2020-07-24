# encoding: utf-8
"""
@auth: cyq
@file: MyRequest.py
@desc: reqparse.Argument, 写方法
"""
import flask_restful
from flask import current_app
from flask_restful import reqparse

class MyArgument(reqparse.Argument):

    def convert(self, value, op):
        """
        重写加入判断是否为空字符串
        """
        if value is None or value == "":
            raise TypeError("%s can't be null" % self.name)
        return super().convert(value, op)


    def handle_validation_error(self, error, bundle_errors):
        """
        自定义错误返回
        """
        err = f"{self.name} 不能为空"
        if current_app.config.get("BUNDLE_ERRORS", False) or bundle_errors:
            return error, err
        flask_restful.abort(400, code=1, data="", err=err)
