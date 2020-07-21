#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/5 16:20
import json

from werkzeug.exceptions import HTTPException


class JsonHTTPException(HTTPException):
    def get_description(self, environ=None):
        """Get the description."""
        return self.description

    def get_body(self, environ=None):
        """Get the HTML body."""
        return json.dumps(
            {"code": self.code, "name": self.name, "msg": self.get_description(environ)}
        )

    def get_headers(self, environ=None):
        """Get a list of headers."""
        return [("Content-Type", "application/json")]


class JsonValidateError(JsonHTTPException):
    """验证不通过"""
    code = 400

class JsonDatabaseError(JsonHTTPException):
    """验证不通过"""
    code = 500