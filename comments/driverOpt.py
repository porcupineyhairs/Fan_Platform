# encoding: utf-8
"""
@auth: cyq
@name: driverOpt
@desc: 用力参数处理
"""
import json
import os

from Model.Models import UMethod, Steps
from comments.Base import PageBase
from comments.log import get_log

log = get_log(__name__)

a = [{'id': 1, 'name': '打开网页', 'desc': '打开网页', 'methodId': None, 'type': None, 'locator': None, 'do': 'get',
      'value': 'http://www.baidu.com', 'variable': None, 'validate': None},
     {'id': 2, 'name': '使用方法', 'desc': None, 'methodId': 1, 'type': None, 'locator': None, 'do': None, 'value': None,
      'variable': None, 'validate': None},
     {'id': 3, 'name': '截图', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'screenshot',
      'value': None, 'variable': None, 'validate': None},
     {'id': 4, 'name': 'get_title', 'desc': None, 'methodId': None, 'type': None, 'locator': None, 'do': 'get_title',
      'value': None, 'variable': 'title', 'validate': '[{"eq": ["title", "python_百度搜索"]}]'}]

from App import create_app, db

create_app().app_context().push()


class DriverOpt(PageBase):

    def run(self, steps):
        try:
            for step in steps:
                self.__run_steps(step)
        except Exception as e:
            log.exception(e)
        finally:
            self.quit_Browser()

    def __run_steps(self, step: dict):
        """
        步骤
        """

        current_step = Steps.get(step['id'])
        do = step["do"]
        if do == "get":
            current_step.log = self.get_url(step['value'])

        elif "methodId" in step and step['methodId']:
            methodSteps = json.loads(UMethod.get(step['methodId']).body)
            self.__run_method_steps(methodSteps)
        elif do == 'screenshot':
            # 截图
            from comments.seve_pic import getPicPath
            path = getPicPath()
            # 判断时候存在
            if current_step.pic:
                os.remove(current_step.pic)
                # 截圖到目錄
            current_step.log = self.Save_Pic(path)
            current_step.pic = path

        elif do == 'click':
            current_step.log = self.click((step['type'], step['locator']))
        elif do == "send_keys":
            current_step.log = self.send_keys((step['type'], step['locator']), step['value'])
        elif do == "sleep":
            current_step.log = self.sleep(step['value'])
        elif do == 'get_text':
            current_step.value, current_step.log = self.get_text((step['type'], step['locator']))

        elif do == 'get_attribute':
            current_step.value, current_step.log = self.get_attribute((step['type'], step['locator']), step['value'])

        elif do == 'refresh':
            current_step.log = self.refresh()

        elif do == 'clear':
            current_step.log = self.clear((step['type'], step['locator']))

        elif do == "switch_to_window":
            self.switch_to_window(step['value'])


        elif do == "get_title":
            current_step.value, current_step.log = self.get_title()

        db.session.commit()

    def __run_method_steps(self, steps: list):
        try:
            for step in steps:
                self.__run_steps(step)
        except Exception as e:
            log.exception(e)


if __name__ == '__main__':
    DriverOpt().run(a)
