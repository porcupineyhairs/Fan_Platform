from flask import Flask
from flask_sqlalchemy import SQLAlchemy, BaseQuery
from flask_httpauth import HTTPBasicAuth
from flask_caching import Cache

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


    import Model.Models
    return app
