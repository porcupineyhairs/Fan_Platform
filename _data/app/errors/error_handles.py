#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/5 16:35
from flask import jsonify
from werkzeug.exceptions import abort

from app import app
from app.errors.exceptions import DatabaseException


@app.errorhandler(DatabaseException)
def database_error(error):
    res = jsonify({"msg":error, "code": "500"})
    res.status = "500"
    return res

