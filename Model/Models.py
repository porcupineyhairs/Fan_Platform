# encoding: utf-8
"""
@auth: cyq
@file: models.py
@desc: 模型
"""
import time

import jwt
from flask import current_app
from werkzeug.security import generate_password_hash, check_password_hash

from App import db


# 用戶
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(32), unique=True, index=True)
    password = db.Column(db.String(128))
    email = db.Column(db.String(52), nullable=True, unique=False)
    phone = db.Column(db.String(12), unique=False, nullable=True)
    gender = db.Column(db.Boolean, default=True, nullable=True)  # 1 男 2 女
    admin = db.Column(db.Boolean, default=False)

    # 所属部门
    part = db.Column(db.Integer, db.ForeignKey("part.id"), nullable=True)

    def __init__(self, username, password, phone=None, email=email, partId=None, admin=None, gender=None):
        self.username = username
        self.part = partId
        self.admin = admin
        self.email = email
        self.gender = gender
        self.phone = phone
        self.hash_password(password)

    def get_userId(self):
        return self.id

    def is_superuser(self):
        return self.admin

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password, password)

    def generate_auth_token(self, expires_in=30):
        return jwt.encode(
            {'id': self.id, 'exp': time.time() + expires_in},
            current_app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_token(token):
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'],
                              algorithms=['HS256'])
        except:
            return None
        return User.query.get(data['id'])

    def __repr__(self):
        return f"username:{self.username}"


# 部门
class Part(db.Model):
    __tablename__ = 'part'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    Part_Name = db.Column(db.String(32), unique=True)
    Part_Users = db.relationship("User", backref="user_part", lazy="dynamic")

    def __init__(self, partName):
        self.Part_Name = partName

    def __repr__(self):
        return f"part:{self.Part_Name}"
