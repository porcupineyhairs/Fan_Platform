# encoding: utf-8
"""
@auth: cyq
@name: driverOpt
@desc: 用力参数处理
"""
import time

from comments.Base import PageBase

a = [{'id': 1, 'name': '打开网页', 'desc': '打开网页', 'methodId': None, 'type': None, 'locator': None, 'do': 'get',
      'value': 'www.baidu.com', 'variable': None, 'validate': None},
     {'id': 2, 'name': '使用方法', 'desc': None, 'methodId': 1, 'type': None, 'locator': None, 'do': None, 'value': None,
      'variable': None, 'validate': None},
     {'id': 3, 'name': '截图', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'screenshot',
      'value': None, 'variable': None, 'validate': None},
     {'id': 4, 'name': 'get title', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'get_title',
      'value': None, 'variable': 'title', 'validate': '[{"eq": ["title", "python_百度搜索"]}]'}]


class DriverOpt(PageBase):

    # def __init__(self, case: dict):
    #     self.__headless = case['headless']
    #     self.__windowsSize = case['windowsSize']
    #     self.__steps = case['steps']
    #     super().__init__()

    def run(self, steps):
        # create_app().app_context().push()
        print(steps)
        try:
            for step in steps:
                self.__run_steps(step)
        except TimeoutError as e:
            print(e)
        finally:
            self.quit_Browser()

    def __run_steps(self, step: dict):
        do = step["do"]

        if do == "get":
            print(step['value'])
            self.getUrl(step['value'])
            time.sleep(5)
        elif do == 'screenshot':
            pass
