# encoding: utf-8
"""
@auth: cyq
@name: caseGenerate
@desc: case参数处理
"""
import json
import os

import yaml
from httprunner import HttpRunner
from httprunner.make import convert_testcase_path

from Model.Models import DebugTalks
from comments.caseParseOpt import CaseParseOpt

par = CaseParseOpt()


class CaseGenerateOpt:

    def __init__(self):
        self.runner = HttpRunner()

    def generateCaseFile(self, caseInfo, casePath: str, env):

        """
        生成目录 构建yml 测试用例
        """
        case_list = {}
        config = {
            "name": caseInfo.name,
            "base_url": env.base_url if env else ""
        }
        case_list['config'] = config

        # steps
        caseRequest = json.loads(caseInfo.request)
        teststeps = []

        for case in caseRequest:
            step = {}
            step['name'] = case['stepName']
            req = dict(url=case['stepUrl'], method=case['stepMethod'], headers=case['stepHeaders'])
            if case['stepJson']:
                req['json'] = case['stepJson']
            elif case['stepParams']:
                req['params'] = case['stepParams']

            step['request'] = req
            step['extract'] = case['stepExtract']
            step['validate'] = [v for v in case['stepValidate']]
            teststeps.append(step)

        case_list['teststeps'] = teststeps
        # 接口名
        caseInterfaceName = caseInfo.getInterfaceInfo.interface_name
        # 项目名
        caseProjectId = caseInfo.project_id
        # caseName
        self.caseName = caseInfo.name
        # caseId
        self.runner.with_case_id(caseInfo.id)

        # 创建
        if not os.path.exists(casePath):
            os.makedirs(casePath)
            debugtalk_obj = DebugTalks.query.get(caseProjectId)
            if debugtalk_obj:
                debugtalk = debugtalk_obj.debugtalk
            else:
                debugtalk = ""

            # 创建debugtalk.py文件
            with open(os.path.join(casePath, 'debugtalk.py'),
                      mode='w',
                      encoding='utf-8') as one_file:
                one_file.write(debugtalk)

        self.caseDirPath = os.path.join(casePath, caseInterfaceName)
        # 在项目目录下创建接口名所在文件夹
        if not os.path.exists(self.caseDirPath):
            os.makedirs(self.caseDirPath)

        self.finallPath = os.path.join(self.caseDirPath, self.caseName + '.yml')
        with open(os.path.join(self.finallPath),
                  mode="w", encoding="utf-8") as one_file:
            yaml.dump(case_list, one_file, allow_unicode=True)

    def run(self):

        self.runner.run_path(self.finallPath)
        res = self.runner.get_summary().dict()
        print(self.caseDirPath)
        print(self.finallPath)

        # alluredir = os.path.join(self.caseDirPath,"alluredir")
        #
        # Shell.invoke(f"hrun {self.finallPath} --alluredir={alluredir}")
        # # 生成report地址
        # AllureReport = os.path.join(self.caseDirPath, "report")
        # # shell执行
        # Shell.invoke(f"allure-2.9.0/bin/allure generate {alluredir} -o  {AllureReport} --clean")

        # index = os.path.join(AllureReport, "index.html")
        # return res, index



