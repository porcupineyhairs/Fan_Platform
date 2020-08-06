# encoding: utf-8
"""
@auth: cyq
@name: driverOpt
@desc: 用力参数处理
"""

from App import create_app

a = [{'id': 1, 'name': '打开网页', 'desc': '打开网页', 'methodId': None, 'type': None, 'locator': None, 'do': 'get',
      'value': 'www.baidu.com', 'variable': None, 'validate': None},
     {'id': 2, 'name': '使用方法', 'desc': None, 'methodId': 1, 'type': None, 'locator': None, 'do': None, 'value': None,
      'variable': None, 'validate': None},
     {'id': 3, 'name': '截图', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'screenshot',
      'value': None, 'variable': None, 'validate': None},
     {'id': 4, 'name': 'get title', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'get_title',
      'value': None, 'variable': 'title', 'validate': '[{"eq": ["title", "python_百度搜索"]}]'}]
from .Base import PageBase


class DriverOpt:

    def __init__(self, case: dict):
        self.__headless = case['headless']
        self.__windowsSize = case['windowsSize']
        self.__steps = case['steps']
        self.__worker = PageBase()

    def run(self):
        create_app().app_context().push()
        for step in self.__steps:
            do = step['do']
            print(do)

