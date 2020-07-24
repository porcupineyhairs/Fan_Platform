# encoding: utf-8
"""
@auth: cyq
@file: caseOpt.py
@desc: 测试用例接口
"""
import json
import os
from datetime import datetime

from flask import request, jsonify, g
from flask_restful import Api, Resource, reqparse

from Model.Models import Case, Interfaces, Envs, Project
from comments.MyRequest import MyArgument
from comments.caseGenerate import CaseGenerateOpt
from comments.caseParseOpt import CaseParseOpt
from comments.log import get_log
from . import v1
from .. import auth, db
log = get_log(__name__)


class CaseOpt(Resource):

    @auth.login_required
    def get(self):
        pass

    @auth.login_required
    def post(self):
        par = CaseParseOpt()
        user = g.user.username
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseName", type=str, required=True, help="caseName 不能为空")
        parse.add_argument("caseInterfaceId", type=str, required=True, help="caseInterfaceId 不能为空")
        parse.add_argument("caseProjectId", type=str, required=True, help="caseProjectId 不能为空")
        parse.add_argument("caseDesc", type=str, default="")
        caseName = parse.parse_args().get("caseName")
        caseDesc = parse.parse_args().get("caseDesc")
        caseInterfaceId = parse.parse_args().get("caseInterfaceId")
        caseProjectId= parse.parse_args().get("caseProjectId")
        # 判断是否重复
        Case.assertName(caseName)

        # 判断caseProjectId,caseInterfaceId
        Project.assertIdExisted(caseProjectId)
        Interfaces.assertIdExisted(caseInterfaceId)

        # 解析step
        caseSteps = request.json.get('caseSteps')
        if not caseSteps:
            return jsonify(dict(code=1, data="", err="caseSteps 不能为空"))

        for step in caseSteps:
            step['stepHeaders'] = par.body_to_dict(step['stepHeaders'])
            step['stepBody'] = par.body_to_dict(step['stepBody'])
            step['stepRequest'] =  par.body_to_dict(step['stepRequest'])
        caseSteps = json.dumps(caseSteps, ensure_ascii=False)

        try:
            case = Case(name=caseName, desc=caseDesc, request=caseSteps, interface_id=caseInterfaceId, author=user)
            case.save()
            return jsonify(dict(code=0, data=case.id, msg='ok'))

        except Exception as e:
            db.session.rollback()
            log.exception(e)
            return jsonify(dict(code=1, data="", err=f"{e}"))
        finally:
            db.session.close()

    @auth.login_required
    def put(self):
        pass

    @auth.login_required
    def delete(self):
        pass


class RunCase(Resource):

    @auth.login_required
    def post(self):
        do = CaseGenerateOpt()
        par = CaseParseOpt()
        user = g.user.username
        caseId = request.json.get("caseId")
        envId = request.json.get("envId")
        if not caseId:
            return jsonify(dict(code=1,data="",err="caseId 不能为空"))

        env = Envs.get(envId)
        case = Case.get(caseId)


        from suite.pwd import get_cwd
        SUITES_DIR = get_cwd()
        case_dir_path = os.path.join(SUITES_DIR,
                                         datetime.strftime(datetime.now(), '%Y-%m-%d-%H-%M-%S-%f'))

        do.generateCaseFile(caseInfo=case,casePath=case_dir_path,env=env)
        return "ok"


api_script = Api(v1)
api_script.add_resource(CaseOpt, "/caseOpt")
api_script.add_resource(RunCase, "/runCase")
