#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 12:18
from flask import render_template, current_app, jsonify, request, session
from flask_login import login_required

from app.main import web
from app.main.models import ProjectInfo


@web.route('/')
@login_required
def index():
    # print(session)
    current_app.logger.warn('你好')
    projects = ProjectInfo.all()
    current_app.logger.info('hahh,正在访问index')
    return render_template('index.html', projects=projects)


@web.route('/demo_login')
def demo_login():
    return jsonify({"token":"login"})

@web.route('/demo')
def demo():
    token = request.headers.get('token', '')
    if not token:
        return jsonify({"msg":"error"})
    return jsonify({"msg":"success"})