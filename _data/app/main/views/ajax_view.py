#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/7/12 11:56
from flask import jsonify, current_app

from app.main import web
from app.errors.json_errors import JsonValidateError
from app.main.models import ProjectInfo, ModuleInfo


@web.route('/modules_by_project/<int:p_id>')
def modules_by_project_id(p_id):
    current_app.logger.warn('正在进行module')
    project = ProjectInfo.get(p_id)
    if project is None:
        raise JsonValidateError()
    modules = project.module_records # status=1
    return jsonify({"data": [{"id": m.id, "name": m.module_name} for m in modules]})


@web.route('/cases_by_module/<int:m_id>')
def cases_by_module(m_id):
    module = ModuleInfo.get(m_id)
    if module is None:
        raise JsonValidateError()
    cases = module.case_records
    return jsonify({"data": [{"id": c.id, "name": c.name} for c in cases]})
