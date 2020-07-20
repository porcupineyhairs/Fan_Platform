# encoding: utf-8
"""
@auth: cyq
@name: moduleOpt
@desc: moduleOpt
"""
from flask import request, jsonify
from flask_restful import Api, Resource

from App.Api.errors_and_auth import is_admin
from Model.Models import Module
from comments.log import get_log
from . import v1
from .. import auth, db

log = get_log(__name__)


class ModuleOpt(Resource):

    @auth.login_required
    def post(self):
        projectId = request.json.get("projectId")
        moduleName = request.json.get('moduleName')
        moduleDesc = request.json.get('moduleDesc')

        if not projectId or not moduleName:
            return jsonify(dict(code=1, err="缺少必传参数"))
        try:
            m = Module(name=moduleName, pid=projectId, desc=moduleDesc)
            return jsonify(dict(code=0, data=f"{m.id}", msg="ok"))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, data="", msg="错误"))
        finally:
            db.session.close()

    @auth.login_required
    def get(self):
        mid = request.args.get("mid")
        try:
            if mid:
                m = [Module.get(mid)]
            else:
                m = Module.all()
            data = {
                "code": 0,
                "msg": "ok",
                "data": [
                    {"id": i.id,"status":i.status, "module_name": i.module_name, "module_desc": i.module_desc, "project_id": i.project_id}
                    for i in m],
                "total":len(m)
            }
            return jsonify(data)

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=1, data="", err=f"错误:{str(e)}"))


    @auth.login_required
    @is_admin
    def delete(self):
        mid = request.json.get('moduleId')
        if not mid:
            return jsonify(dict(code=1, err="缺少必传参数"))

        try:
            m = Module.get(mid)
            m.delete()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"{e}"))

    @auth.login_required
    def put(self):
        mid = request.json.get('moduleId')
        moduleName = request.json.get('moduleName')
        moduleDesc = request.json.get("moduleDesc")
        if not mid:
            return jsonify(dict(code=1, err="缺少必传参数"))
        try:
            m = Module.get(mid)
            m.module_name = moduleName
            m.module_desc = moduleDesc
            m.save()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, err=f"{e}"))

        finally:
            db.session.close()
api_script = Api(v1)
api_script.add_resource(ModuleOpt, "/moduleOpt")
