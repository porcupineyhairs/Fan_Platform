import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from comments.config import config

db = SQLAlchemy()
app = Flask(__name__)
db.init_app(app)
app.config.from_object(config['testing'])
app.config['SECRET_KEY'] = os.urandom(15)
