# encoding: utf-8
"""
@auth: cyq
@name: projectOpt
@desc: 项目接口
"""

from flask import jsonify, request
from flask_restful import Api, Resource

from Model.Models import Project
from comments.log import get_log
from . import v1
from .errors_and_auth import is_admin
from .. import auth, db

log = get_log(__file__)


class ProjectOpt(Resource):

    @auth.login_required
    def get(self):
        """
        获取project  id,[id,id].None 三种
        """
        try:
            pid = request.args.get("projectId")
            if pid:
                projects = [Project.get(pid)]
            else:
                projects = Project.all()
            data = {
                "code": 0,
                "msg": "ok",
                "data": [
                    {"id": i.id, "status": i.status, "project_name": i.project_name, "project_desc": i.project_desc} for
                    i
                    in projects]
            }
            return jsonify(data)
        except Exception as e:
            db.session.rollback()
            log.exception(str(e))
            return jsonify(dict(code=1, err=f"错误:{str(e)}"))

    @auth.login_required
    @is_admin
    def post(self):
        pName = request.json.get("projectName")
        pDesc = request.json.get("projectDesc")

        if not pDesc or not pName:
            return jsonify(dict(code=1, err="传入必传"))

        p = Project.query.filter(Project.project_name == pName).first()
        if p:
            return jsonify(dict(code=1, err="projectName存在了"))
        try:
            Project(name=pName, desc=pDesc).save()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"{e}"))

    @auth.login_required
    @is_admin
    def put(self):
        pName = request.json.get("projectName")
        pDesc = request.json.get("projectDesc")
        pId = request.json.get('projectId')

        if not pId:
            return jsonify(dict(code=1, err="传入必传"))

        try:
            p = Project.get(pId)
            p.project_name = pName
            p.project_desc = pDesc
            db.session.commit()
            return jsonify(dict(code=0, data=p.id, msg="ok"))

        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"{e}"))

    @auth.login_required
    @is_admin
    def delete(self):
        projectId = request.json.get('projectId')
        if not projectId:
            return jsonify(dict(code=1, err="projectId不能为空"))
        try:
            p = Project.get(projectId)
            p.delete()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"{e}"))


api_script = Api(v1)
api_script.add_resource(ProjectOpt, "/projectOpt")