# encoding: utf-8
"""
@auth: cyq
@name: caseGenerate
@desc: 用力参数处理
"""
import json
import os

import yaml

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
        print(caseRequest)
        """
        [{'stepName': '图灵接口测试', 
        'stepDesc': 'step_desc', 
        'stepUrl': 
        'http://www.tuling123.com/openapi/api', 
        'stepMethod': 'POST', 
        'stepHeaders': {'Content-Type': 'application/json'}, 
        'stepJson':{'key': '8fe3b232710c4c0d87b761ed5301e7a4', 'info': '你叫什么', 'userid': '123456'}
        'stepParams': '', 
        'stepResponse': {'code': 100000, 'text': '我是棒棒哒图灵机器人'}, 
        'stepValidate': [{'eq': ['status_code', 200]}, {'eq': ['body.text', '我是棒棒哒图灵机器人']}, {'eq': ['code', 10000]}]
        'stepValidate_script': ['assert status_code == 200', "'我是棒棒哒图灵机器人' = response_json.get('text')"], 
        'stepExtract': '', 
        """

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
        caseName = caseInfo.name

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

        caseDirPath = os.path.join(casePath, caseInterfaceName)
        # 在项目目录下创建接口名所在文件夹
        if not os.path.exists(caseDirPath):
            os.makedirs(caseDirPath)

        with open(os.path.join(caseDirPath, caseName + '.yml'),
                  mode="w", encoding="utf-8") as one_file:
            yaml.dump(case_list, one_file, allow_unicode=True)

    def __validateOpt(self):
        """
         {"status_code": 200, "mode": "eq", "body.text": "我是棒棒哒图灵机器人", "code": 10000}
         - eq: ["status_code", 200]
        """
