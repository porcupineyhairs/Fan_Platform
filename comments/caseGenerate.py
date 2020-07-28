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

from Model.Models import DebugTalks
from comments.caseParseOpt import CaseParseOpt

par = CaseParseOpt()


class CaseGenerateOpt:

    def generateCaseFile(self, caseInfo, casePath: str, env):
        """
        生成目录 构建yml 测试用例
        """
        case_list = {}
        config =  {
                "name": caseInfo.name,
                "base_url": env.base_url if env else ""
        }
        case_list['config'] = config

        # steps
        caseRequest = json.loads(caseInfo.request)

        teststeps = []
        step = {}

        for case in caseRequest:
            step['name'] = case['stepName']
            step['request'] = dict(url=case['stepUrl'], method=case['stepMethod'], headers=case['stepHeaders'],
                                   json=case['stepJson'], params=case['stepParams'])
            step['validate'] = [v  for v in case['stepValidate']]
            teststeps.append(step)

        case_list['teststeps'] = teststeps
        # 接口名
        caseInterfaceName = caseInfo.getInterfaceInfo.interface_name
        # 项目名
        caseProjectId = caseInfo.project_id
        # caseName
        self.caseName = caseInfo.name

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

        self.finallPath = os.path.join(self.caseDirPath,self.caseName+'.yml')
        with open(os.path.join(self.finallPath),
                  mode="w", encoding="utf-8") as one_file:
            yaml.dump(case_list, one_file, allow_unicode=True)

    def run(self):
        h =HttpRunner().run_path(self.finallPath)

