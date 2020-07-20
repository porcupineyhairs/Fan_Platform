# encoding: utf-8
"""
@auth: cyq
@file: caseOpt.py
@desc: 测试用例接口
"""
from .. import auth,db
from . import v1
from flask_restful import Api,Resource


class CaseOpt(Resource):

    @auth.login_required
    def get(self):
        pass


    @auth.login_required
    def post(self):
        pass

    @auth.login_required
    def put(self):
        pass

    @auth.login_required
    def delete(self):
        pass










api_script = Api(v1)
api_script.add_resource(CaseOpt,"/caseOpt")
