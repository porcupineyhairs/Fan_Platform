# encoding: utf-8
"""
@auth: cyq
@name: __init__
@desc: 工厂模式 初始化
"""

from celery import Celery
from flask import Flask
from flask_caching import Cache
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
    db.init_app(app)
    catch.init_app(app)

    from .Api import v1
    app.register_blueprint(v1)

    return app


def create_celery_app():
    app = create_app()
    celery = Celery(app.name, broker=app.config["CELERY_BROKER_URL"])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return super().__call__(*args, **kwargs)

    celery.Task = ContextTask
    return celery

