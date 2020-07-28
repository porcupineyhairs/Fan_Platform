# encoding: utf-8
"""
@auth: cyq
@file: caseOpt.py
@desc: 测试用例接口
"""
import json

from flask import request, jsonify, g
from flask_restful import Api, Resource, reqparse

from App.Api.errors_and_auth import is_admin
from Model.Models import Case, Interfaces, Envs, Project
from comments.MyRequest import MyArgument
from comments.caseParseOpt import CaseParseOpt
from comments.log import get_log
from . import v1
from .. import auth, db

log = get_log(__name__)


class CaseOpt(Resource):

    @auth.login_required
    def get(self):
        caseId = request.args.get("caseId")
        try:
            if caseId:
                case = [Case.get(caseId)]
            else:
                case = Case.all()

            data = {
                "code": 0,
                "msg": "ok",
                "data": [
                    {"id": i.id, "status": i.status,"author":i.author, "name": i.name, "desc": i.desc, "request":
                        json.loads(
                        i.request),
                     "project_id": i.project_id, "interface_id": i.interface_id} for i in case]}

            return jsonify(data)

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=1, data="", err=f"错误:{str(e)}"))

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
        caseProjectId = parse.parse_args().get("caseProjectId")
        # 判断是否重复
        Case.assertName(caseName)

        # 判断caseProjectId,caseInterfaceId
        Project.assertIdExisted(caseProjectId)
        Interfaces.assertIdExisted(caseInterfaceId)

        # 解析step
        caseSteps = request.json.get('caseSteps')
        if not caseSteps:
            return jsonify(dict(code=1, data="", err="caseSteps 不能为空"))

        # 参数处理
        for step in caseSteps:
            step['stepHeaders'] = par.body_to_dict(step['stepHeaders'])
            step['stepJson'] = par.body_to_dict(step['stepJson'])
            step['stepParams'] = par.body_to_dict(step['stepParams'])
            step['stepValidate'] = par.validate_to_dict(step['stepValidate'])

        caseSteps = json.dumps(caseSteps, ensure_ascii=False)

        try:
            case = Case(name=caseName, desc=caseDesc, request=caseSteps, interface_id=caseInterfaceId,
                        project_id=caseProjectId,
                        author=user)
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
        par = CaseParseOpt()
        user = g.user.username
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseId", type=int, required=True, help="caseId 不能为空")
        parse.add_argument("caseName", type=str, required=True, help="caseName 不能为空")
        parse.add_argument("caseDesc", type=str, default="")
        caseId = parse.parse_args().get('caseId')
        caseName = parse.parse_args().get("caseName")
        caseDesc = parse.parse_args().get("caseDesc")
        # 判断是否重复
        Case.assertName(caseName)

        # 解析step
        caseSteps = request.json.get('caseSteps')
        if not caseSteps:
            return jsonify(dict(code=1, data="", err="caseSteps 不能为空"))

        # 参数处理
        for step in caseSteps:
            step['stepHeaders'] = par.body_to_dict(step['stepHeaders'])
            step['stepJson'] = par.body_to_dict(step['stepJson'])
            step['stepParams'] = par.body_to_dict(step['stepParams'])
            step['stepValidate'] = par.validate_to_dict(step['stepValidate'])

        caseSteps = json.dumps(caseSteps, ensure_ascii=False)

        try:
            case = Case.get(caseId)
            case.name = caseName
            case.desc = caseDesc
            case.request = caseSteps
            case.save()
            return jsonify(dict(code=0, data=case.id, msg='ok'))

        except Exception as e:
            db.session.rollback()
            log.exception(e)
            return jsonify(dict(code=1, data="", err=f"{e}"))
        finally:
            db.session.close()

    @auth.login_required
    @is_admin
    def delete(self):
        user = g.user.username
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseId", type=int, required=True, help="caseId 不能为空")
        caseId = parse.parse_args().get('caseId')

        try:
            Case.get(caseId).delete()
            return jsonify(dict(code=0, data="", msg='ok'))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=1, err=f"错误:{str(e)}"))
        finally:
            db.session.close()


class RunCase(Resource):

    @auth.login_required
    def post(self):
        par = CaseParseOpt()
        user = g.user.username
        caseId = request.json.get("caseId")
        envId = request.json.get("envId")
        if not caseId:
            return jsonify(dict(code=1, data="", err="caseId 不能为空"))

        env = Envs.get(envId)
        case = Case.get(caseId)

        from comments.caseGenerate import CaseGenerateOpt
        from suite.pwd import get_cwd

        caseName = case.name
        caseSteps = case.request
        # do = Runner(caseName=caseName, caseSteps=caseSteps, env=env).setParams()
        do = CaseGenerateOpt()
        do.generateCaseFile(caseInfo=case, casePath=get_cwd(), env=env)
        do.run()
        return "ok"


api_script = Api(v1)
api_script.add_resource(CaseOpt, "/caseOpt")
api_script.add_resource(RunCase, "/runCase")
