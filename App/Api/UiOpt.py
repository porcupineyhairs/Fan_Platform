# encoding: utf-8
"""
@auth: cyq
@file: UiOpt.py
@desc: UI自动化用例接口
"""
import json
import os

from flask import request, jsonify, g, send_file, safe_join
from flask_restful import Resource, Api, reqparse

from App import auth, db
from Model.Models import Project, UMethod, UICase, Steps
from comments.MyRequest import MyArgument
from comments.Verify import Verify
from comments.driverOpt import DriverOpt
from comments.log import get_log
from . import v1

log = get_log(__name__)


class UiCase(Resource):

    @auth.login_required
    def post(self):
        creator = g.user.username
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("projectId", type=str, required=True, help="projectId 不能为空")
        parse.add_argument("caseName", type=str, required=True, help="caseName 不能为空")
        parse.add_argument("caseDesc", type=str, default="")
        parse.add_argument("headless", type=str, default=False)
        parse.add_argument("windowsSize", type=str, default=None)

        headless = parse.parse_args().get("headless")
        windowsSize = parse.parse_args().get("windowsSize")

        projectId = parse.parse_args().get('projectId')
        Project.assertIdExisted(projectId)

        caseName = parse.parse_args().get('caseName')
        UICase.assertName(caseName)

        caseDesc = parse.parse_args().get('caseDesc')
        steps = self._del_step_info(request.json.get('caseSteps'))

        try:
            u = UICase(name=caseName, desc=caseDesc, creator=creator, project_id=projectId, headless=headless,
                       windowsSize=windowsSize)
            for step in steps:
                s = Steps(name=step['name'], desc=step['desc'], is_method=step['is_method'],
                          type=step['type'], locator=step['locator'], do=step['do'], value=step['value'],
                          variable=step['variable'], validate=step['validate'])
                u.casesteps.append(s)
            u.save()

            return jsonify(dict(code=1, data=u.id, msg='ok'))

        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, err=f"错误:{str(e)}"))
        finally:
            db.session.close()

    def get(self):
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseId", type=str, required=False, help="caseId 不能为空")
        parse.add_argument("steps", type=str)
        caseId = parse.parse_args().get("caseId")
        steps = parse.parse_args().get("steps")

        data = {'code': 1, "data": []}
        try:
            if caseId:
                u = [UICase.get(caseId)]

            else:
                u = UICase.all()
            data['data'] = [
                {"id": i.id, "projectId": i.project_id, "name": i.name, "desc": i.desc, "creator": i.creator,
                 "headless": i.headless, "windowsSize": i.windowsSize,
                 "status": i.status, "state": i.state,
                 "steps": [{"id": s.id, "name": s.name, "desc": s.desc, "methodId": s.is_method, "type": s.type,
                            "locator": s.locator,
                            "do": s.do, "value": s.value, "variable": s.variable, "validate": s.validate} for s in
                           i.casesteps if steps]}
                for i in u]
            return jsonify(data)

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"错误:{str(e)}"))

    @auth.login_required
    def put(self):
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseId", type=str, required=True, help="caseId 不能为空")
        parse.add_argument("caseName", type=str, required=True, help="caseName 不能为空")
        parse.add_argument("caseDesc", type=str, default="")
        parse.add_argument("headless", type=bool, default=False)
        parse.add_argument("windowsSize", type=str, default=None)

        caseId = parse.parse_args().get("caseId")
        headless = parse.parse_args().get("headless")
        windowsSize = parse.parse_args().get("windowsSize")
        caseName = parse.parse_args().get('caseName')
        caseDesc = parse.parse_args().get('caseDesc')
        steps = self._del_step_info(request.json.get('caseSteps'))

        try:
            u = UICase.get(caseId)
            u.name = caseName
            u.desc = caseDesc
            u.headless = headless
            u.windowsSize = windowsSize
            u.state = "stay"

            # 刪除已存在
            u.delete_steps()
            # for step in steps:
            #     s = Steps.get(step['id'])
            #     s.name = step['name']
            #     s.desc = step['desc']
            #     s.is_method = step['is_method']
            #     s.type = step['type']
            #     s.locator = step['locator']
            #     s.do = step['do']
            #     s.value = step['value']
            #     s.variable = step['variable']
            #     s.validate = step['validate']
            for step in steps:
                s = Steps(name=step['name'], desc=step['desc'], is_method=step['is_method'],
                          type=step['type'], locator=step['locator'], do=step['do'],
                          variable=step['variable'], validate=step['validate'])

                if isinstance(step['value'], list):
                    s.value = json.dumps(step['value'], ensure_ascii=False)
                else:
                    s.value = step['value']
                u.casesteps.append(s)
            u.save()

            db.session.commit()
            return jsonify(dict(code=1, data=u.id, msg='ok'))

        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, data="", err=f"错误:{e}"))
        finally:
            db.session.close()

    @auth.login_required
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseId", type=str, required=True, help="caseId 不能为空")
        caseId = parse.parse_args().get("caseId")
        try:
            UICase.get(caseId).Delete()
            return jsonify(dict(code=1, msg="ok"))

        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, err=f"错误:{str(e)}"))
        finally:
            db.session.close()

    def _del_step_info(self, steps: list) -> list:
        """
        补充参数
        """
        newList = []
        for step in steps:
            s = {"name": None, "desc": None, "do": None, "is_method": None, "type": None, "locator": None,
                 "value": None, "variable": None, "validate": None}
            for k, v in step.items():
                if k == "validate":
                    v = json.dumps(v, ensure_ascii=False)
                s[k] = v
            newList.append(s)
        return newList


class Method(Resource):

    @auth.login_required
    def post(self):
        creator = g.user.username
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("ProjectId", type=str, required=True, help="ProjectId 不能为空")
        parse.add_argument("methodName", type=str, required=True, help="methodName 不能为空")
        parse.add_argument("methodDesc", type=str, default="")
        ProjectId = parse.parse_args().get('ProjectId')
        methodName = parse.parse_args().get('methodName')
        methodDesc = parse.parse_args().get('methodDesc')
        body = json.dumps(request.json.get("methodBody"), ensure_ascii=False)
        try:
            u = UMethod(pid=ProjectId, name=methodName, desc=methodDesc, body=body, creator=creator)
            u.save()
            return jsonify(dict(code=0, data=u.id, msg="ok"))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=1, data="", msg=f"错误:{str(e)}"))
        finally:
            db.session.close()

    @auth.login_required
    def put(self):
        updater = g.user.username
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("methodId", type=str, required=True, help="methodId 不能为空")
        parse.add_argument("methodName", type=str, required=True, help="methodName 不能为空")
        parse.add_argument("methodDesc", type=str, default="")
        methodId = parse.parse_args().get('methodId')
        methodName = parse.parse_args().get('methodName')
        methodDesc = parse.parse_args().get('methodDesc')
        try:
            m = UMethod.get(methodId)
            m.name = methodName
            m.desc = methodDesc
            m.body = json.dumps(request.json.get("methodBody"), ensure_ascii=False)
            m.updater = updater
            m.save()
            return jsonify(dict(code=1, data=m.id, msg="ok"))

        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, err=f"错误:{str(e)}"))
        finally:
            db.session.close()

    @auth.login_required
    def delete(self):
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("methodId", type=str, required=True, help="methodId 不能为空")
        methodId = parse.parse_args().get('methodId')

        try:
            UMethod.get(methodId).Delete()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=1, data="", msg=f"错误:{str(e)}"))
        finally:
            db.session.close()

    def get(self):
        methodId = request.args.get("methodId")
        data = {"code": 0}
        try:
            if methodId:
                m = [UMethod.get(methodId)]
            else:
                m = UMethod.all()

            data['data'] = [{"projectId": i.project_id, "id": i.id, "status": i.status, "name": i.name, "desc": i.desc,
                             "methodBody": json.loads(i.body),
                             "creator": i.creator} for i in m]
            return jsonify(data)

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=1, data="", msg=f"错误:{str(e)}"))


class Run(Resource):

    def post(self):
        caseId = request.json.get('caseId')
        back = request.json.get("back")
        case = UICase.get(caseId)
        case.case_state = "Running"
        db.session.commit()

        if back:
            try:
                from App.celeryOpt import runCase
                runCase.apply_async(args=[caseId])
                return jsonify(dict(code=0, msg='运行成功', caseId=case.id))
            except Exception as e:
                return jsonify(dict(code=1, data="", msg=f"错误:{str(e)}"))

        else:
            try:
                case = UICase.get(caseId)
                info = case.caseInfo
                driver = DriverOpt(headless=info['headless'])
                driver.run(caseId, info["steps"])

                return jsonify(dict(code=0, msg='运行完成', caseId=case.id))
            except Exception as e:
                return jsonify(dict(code=1, data="", msg=f"错误:{str(e)}"))


class Report(Resource):

    def get(self):
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("caseId", type=str, required=True, help="caseId 不能为空")
        caseId = parse.parse_args().get('caseId')

        u = UICase.get(caseId)

        if u.state != "over":
            return jsonify(dict(code=0, msg='用例未运行或运行中。'))

        info = u.get_steps_info
        for stepInfo in info['caseSteps']:
            if stepInfo['validate']:
                stepInfo['verify'], stepInfo['verifyData'] = Verify(stepInfo).verify()

        return jsonify(dict(code=0, msg='ok', data=info))


@v1.route("/getPic/<path:url>")
def getPic(url):
    basedir = os.path.abspath(os.path.dirname(__name__))
    file_path = safe_join(basedir, url)

    return send_file(file_path)


api_script = Api(v1)
api_script.add_resource(UiCase, '/uCaseOpt')
api_script.add_resource(Method, '/methodOpt')
api_script.add_resource(Run, "/run")
api_script.add_resource(Report, "/uReport")
