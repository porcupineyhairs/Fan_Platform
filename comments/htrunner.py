# encoding: utf-8
"""
@auth: cyq
@file: htrunner.py
@desc: httprunner 类
"""
import json

from httprunner import HttpRunner, Config, Step, RunRequest


class Runner(HttpRunner):
    config = None
    teststeps = []

    def __init__(self, caseName: str, caseSteps: str, env=None):
        self.caseName = caseName
        self.caseSteps = caseSteps
        self.env = env
        """
        [{"stepName": "请求", 
        "stepDesc": "step_desc",
        "stepUrl": "http://www.tuling123.com/openapi/api", 
        "stepMethod": "POST", 
        "stepHeaders": {"Content-Type": "application/json"}, 
        "stepBody": "key": "8fe3b232710c4c0d87b761ed5301e7a4", 
        "info": "你叫什么", "userid": "123456"}, 
        "stepRequest": "", 
        "stepResponse": {"code": 100000, "text": "我是棒棒哒图灵机器人"}, 
        "stepJsonpath": "", "stepValidate": [], "stepExtract": ""}]"""

