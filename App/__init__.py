# encoding: utf-8
"""
@auth: cyq
@name: __init__
@desc: 工厂模式 初始化
"""
from flask import Flask
from flask_caching import Cache
from flask_cors import CORS
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from comments.MyBaseQueryOpt import MyBaseQuery
from comments.config import config

db = SQLAlchemy(query_class=MyBaseQuery)
auth = HTTPBasicAuth()
catch = Cache()


def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    CORS(app, supports_credentials=True)  # 设置跨域
    db.init_app(app)
    catch.init_app(app)

    from .Api import v1
    app.register_blueprint(v1)

    return app

