# encoding: utf-8
"""
@auth: cyq
@name: driverOpt
@desc: 用力参数处理
"""
import time

from App import create_app
from comments.log import get_log
from comments.Base import PageBase

log = get_log(__name__)

a = [{'id': 1, 'name': '打开网页', 'desc': '打开网页', 'methodId': None, 'type': None, 'locator': None, 'do': 'get',
      'value': 'www.baidu.com', 'variable': None, 'validate': None},
     {'id': 2, 'name': '使用方法', 'desc': None, 'methodId': 1, 'type': None, 'locator': None, 'do': None, 'value': None,
      'variable': None, 'validate': None},
     {'id': 3, 'name': '截图', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'screenshot',
      'value': None, 'variable': None, 'validate': None},
     {'id': 4, 'name': 'get title', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'get_title',
      'value': None, 'variable': 'title', 'validate': '[{"eq": ["title", "python_百度搜索"]}]'}]


class DriverOpt(PageBase):

    def run(self, steps):
        print(steps)
        try:
            for step in steps:
                self.__run_steps(step)
        except Exception as e:
            log.exception(e)
        finally:
            self.quit_Browser()

    def __run_steps(self, step: dict):
        do = step["do"]
        print(do)
        if do == "get":
            print(step['value'])
            self.get_url(step['value'])
            time.sleep(5)
        elif do == 'screenshot':
            pass
