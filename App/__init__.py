from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPBasicAuth
from flask_caching import Cache
from comments.config import config

db = SQLAlchemy()
auth = HTTPBasicAuth()
catch = Cache()

def create_app(config_name="default"):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    db.init_app(app)
    catch.init_app(app)

    from .Api import v1
    app.register_blueprint(v1)

    # 添加一个过滤器
    from App.Api.temp import str_time
    app.add_template_filter(str_time)

    import Model.Models
    return app


""" app_config
    {'ENV': 'production', 
    'DEBUG': True, 
    'TESTING': False, 
    'PROPAGATE_EXCEPTIONS': None,
     'PRESERVE_CONTEXT_ON_EXCEPTION': None, 
     'SECRET_KEY': 'hard to guess string',
     'PERMANENT_SESSION_LIFETIME': datetime.timedelta(31), 
     'USE_X_SENDFILE': False, 'SERVER_NAME': None,
     'APPLICATION_ROOT': '/', 
     'SESSION_COOKIE_NAME': 'session', 
     'SESSION_COOKIE_DOMAIN': None,
     'SESSION_COOKIE_PATH': None, 
     'SESSION_COOKIE_HTTPONLY': True, 
     'SESSION_COOKIE_SECURE': False,
     'SESSION_COOKIE_SAMESITE': None, 
     'SESSION_REFRESH_EACH_REQUEST': True, 
     'MAX_CONTENT_LENGTH': None,
     'SEND_FILE_MAX_AGE_DEFAULT': datetime.timedelta(0, 43200),
     'TRAP_BAD_REQUEST_ERRORS': None,
     'TRAP_HTTP_EXCEPTIONS': False, 
     'EXPLAIN_TEMPLATE_LOADING': False,
     'PREFERRED_URL_SCHEME': 'http',
     'JSON_AS_ASCII': False, 
     'JSON_SORT_KEYS': True, 
     'JSONIFY_PRETTYPRINT_REGULAR': False,
     'JSONIFY_MIMETYPE': 'application/json', 
     'TEMPLATES_AUTO_RELOAD': None, 'MAX_COOKIE_SIZE': 4093,
     
     'SQLALCHEMY_COMMIT_ON_TEARDOWN': True,
     'SQLALCHEMY_DATABASE_URI': 'sqlite:////home/mi/PycharmProjects/Fan_Platform/comments/data-dev.sqlite',
     'SQLALCHEMY_TRACK_MODIFICATIONS': False, 
     'SQLALCHEMY_BINDS': None, 
     'SQLALCHEMY_NATIVE_UNICODE': None,
     'SQLALCHEMY_ECHO': False, 
     'SQLALCHEMY_RECORD_QUERIES': None, 
     'SQLALCHEMY_POOL_SIZE': None,
     'SQLALCHEMY_POOL_TIMEOUT': None, 
     'SQLALCHEMY_POOL_RECYCLE': None, 
     'SQLALCHEMY_MAX_OVERFLOW': None,
     'SQLALCHEMY_ENGINE_OPTIONS': {}}
"""
