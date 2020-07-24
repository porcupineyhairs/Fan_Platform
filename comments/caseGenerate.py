# encoding: utf-8
"""
@auth: cyq
@name: caseGenerate
@desc: 用力参数处理
"""
import json
import os

import httprunner
import yaml

from Model.Models import DebugTalks
from comments.caseParseOpt import CaseParseOpt

par = CaseParseOpt()

class CaseGenerateOpt:

    def generateCaseFile(self,caseInfo, casePath, env):
        case_list = []
        config = {
            "config": {
                "name": caseInfo.name,
                "requests": {
                    "base_url": env.base_url if env else ""
                }

            }
        }
        case_list.append(config)

        # steps
        caseRequest =  json.loads(caseInfo.request)
        print(caseRequest)
        """
        [{'stepName': '请求',
         'stepDesc': 'step_desc',
          'stepUrl': 'http://www.tuling123.com/openapi/api',
           'stepMethod': 'POST',
            'stepHeaders': {'Content-Type': 'application/json'},
             'stepBody': {'key': '8fe3b232710c4c0d87b761ed5301e7a4', 'info': '今天天气怎么样', 'loc': '北京中关村', 'userid': '123456'}, 'stepRequest': '', 'stepResponse': {'code': 100000, 'text': '请问你想查询哪个城市'},
              'stepJsonpath': '',
               'stepExtract': ''}]"""

        # 接口名
        caseInterfaceName = caseInfo.getInterfaceInfo.interface_name
        # 项目名
        caseProjectId = caseInfo.project_id
        # caseName
        caseName = caseInfo.name


        # # 创建
        # if not os.path.exists(casePath):
        #     os.makedirs(casePath)
        #     debugtalk_obj = DebugTalks.query.get(caseProjectId)
        #     if debugtalk_obj:
        #         debugtalk = debugtalk_obj.debugtalk
        #     else:
        #         debugtalk = ""
        #
        #         # 创建debugtalk.py文件
        #         with open(os.path.join(casePath, 'debugtalk.py'),
        #                   mode='w',
        #                   encoding='utf-8') as one_file:
        #             one_file.write(debugtalk)
        # caseDirPath = os.path.join(casePath, caseInterfaceName)
        # # 在项目目录下创建接口名所在文件夹
        # if not os.path.exists(caseDirPath):
        #     os.makedirs(caseDirPath)
        #
        # with open(os.path.join(caseDirPath, instance.name + '.yml'),
        #           mode="w", encoding="utf-8") as one_file:
        #     yaml.dump(case_list, one_file, allow_unicode=True)


        #https://docs.httprunner.org/installation/



    httprunner
