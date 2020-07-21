#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 11:23
import logging
from logging.handlers import TimedRotatingFileHandler

from flask import Flask
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf import CSRFProtect

from app.config import config

from app.main.models import db, login_manager
from app.main.template_env import str_time, json_loads

app = Flask(__name__)

migrate = Migrate()
mcsrf = CSRFProtect()


def init_log(path, time_out='D'):
    """初始化 logger """
    server_log = TimedRotatingFileHandler(path, time_out)
    server_log.setLevel(logging.DEBUG)
    server_log.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    return server_log


def create_app():
    # 获取配置文件
    app.config.from_object(config)
    # 初始化 log
    log = init_log(app.config['LOG_NAME'])
    app.logger.addHandler(log)
    # 初始化db
    db.init_app(app)
    migrate.init_app(app, db)

    from app.main import web
    app.register_blueprint(web)

    # csrf 保护
    mcsrf.init_app(app)
    # 初始化migrate
    # 注册蓝图
    # 注册过滤器
    app.add_template_filter(str_time)
    # 注册错误处理
    # @app.add_template_global
    app.add_template_global(json_loads)

    login_manager.init_app(app)
    return app
