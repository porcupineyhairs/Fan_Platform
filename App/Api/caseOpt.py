# encoding: utf-8
"""
@auth: cyq
@file: caseOpt.py
@desc: 测试用例接口
"""
from flask import request, g
from flask_restful import Api, Resource

from . import v1
from .. import auth


class CaseOpt(Resource):

    @auth.login_required
    def get(self):
        pass

    @auth.login_required
    def post(self):
        caseInfo = request.json()
        caseAuthor = g.user.username
        caseName = caseInfo.get("caseName")
        caseDesc = caseInfo.get('caseDesc')
        caseInclude = caseInfo.get("caseInclude")
        caseRequest = caseInfo.get("caseRequest")
        caseRequestData = caseInfo.get('caseRequestData')

        caseValidate = caseInfo.get('caseValidate')
        # 将[{'check': 'status_code', 'expected':200, 'comparator': 'equals'}]
        # 转化为[{key: 'status_code', value: 200, comparator: 'equals', param_type: 'string'}]
        caseValidateList = caseValidate

        # 处理param
        caseParams = caseInfo.get('caseParams')
        caseParamsList = caseParams

        # header
        caseParams = caseInfo.get('caseHeaders')
        caseParamsList = caseParams

        #variables 变量
        caseVariables = caseInfo.get('caseVariables')
        caseVariablesList = caseVariables

        # form 表单数据
        caseFormData = caseInfo.get("caseData")

        # json
        caseJson = caseInfo.get('json')

        # extract
        caseExtract = caseInfo.get('caseExtract')

        # parameters



    @auth.login_required
    def put(self):
        pass

    @auth.login_required
    def delete(self):
        pass


api_script = Api(v1)
api_script.add_resource(CaseOpt, "/caseOpt")
