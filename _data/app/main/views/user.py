#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# datetime:2019/8/16 10:07
# email: wagyu2016@163.com
# author: 雨泽
# copyright: 湖南省零檬信息技术有限公司
from flask import request, render_template, redirect
from flask_login import login_user

from app.main import web
from app.main.forms import UserRegisterEmailForm
from app.main.models import User


@web.route('/register', methods=['GET', 'POST'])
def register():
    # 验证
    form = UserRegisterEmailForm()
    # 明文密码 form.data.pwd, js, md 1234==>122234323
    if request.method == 'GET':
        return render_template('register.html', form=form)
    if not form.validate():
        return render_template('register.html', form=form)
    # 写入新用户信息
    user = User.insert(form)
    # 用户激活
    # user_id = user.id
    login_user(user)
    return redirect('/')


# @web.route('/confirm_register/<int:u_id>', methods=['GET', 'POST'])
# def confirm_register(u_id):
#     """注册验证码确认。"""
#     if request.method == 'GET':
#         return 'confirm'
#     code = request.form.get('code')
#     # 如果 code == user.code
#     # 激活
#     return 'confirm again'


@web.route('/login', methods=['GET', 'POST'])
def login():
    # 验证
    form = UserRegisterEmailForm()
    if request.method == 'GET':
        return render_template('login.html', form=form)
    if not form.validate():
        return render_template('login.html', form=form)

    user = User.query.filter_by(email=form.email.data).first()
    if user and user.check_pwd(form.pwd.data):
        # 手动实现登录： session['user'] = user.id
        # flask-login
        # session['user'] = user.id
        login_user(user)
        return redirect('/')
    return render_template('login.html', form=form)


