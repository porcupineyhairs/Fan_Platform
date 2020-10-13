# encoding: utf-8
"""
@auth: cyq
@name: projectOpt
@desc: 项目接口
"""

from flask import jsonify, request
from flask_restful import Api, Resource, reqparse

from Model.Models import Project
from comments.MyRequest import MyArgument
from comments.log import get_log
from . import v1
from .errors_and_auth import is_admin
from .. import auth, db

log = get_log(__file__)


class ProjectOpt(Resource):

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
        parse = reqparse.RequestParser(argument_class=MyArgument)
        parse.add_argument("projectName", type=str, required=True, help="methodId 不能为空")
        parse.add_argument("projectDesc", type=str)
        projectName = parse.parse_args().get('projectName')
        projectDesc = parse.parse_args().get('projectDesc')

        Project.assertName(projectName)

        try:
            Project(name=projectName, desc=projectDesc).save()
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


class ProjectDel(Resource):

    @auth.login_required
    @is_admin
    def post(self):
        projectId = request.json.get('projectId')
        if not projectId:
            return jsonify(dict(code=1, err="projectId不能为空"))

        try:
            if isinstance(projectId, (str, int)):
                Project.assertIdExisted(projectId).Delete()

                return jsonify(dict(code=0, data="", msg="ok"))
            elif isinstance(projectId, list):
                for i in projectId:
                    Project.assertIdExisted(i).Delete()
                return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"{e}"))


api_script = Api(v1)
api_script.add_resource(ProjectOpt, "/projectOpt")
api_script.add_resource(ProjectDel, "/delProject")
