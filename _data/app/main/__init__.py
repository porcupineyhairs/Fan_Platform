#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 13:46
from flask import Blueprint

web = Blueprint('web', __name__)

from app.main.views import index, cases, modules, projects, suites, ajax_view, user