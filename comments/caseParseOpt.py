# encoding: utf-8
"""
@auth: cyq
@name: caseParseOpt
@desc: 用力参数处理
"""
import json


class CaseParseOpt:

    def body_to_dict(self, d: list):
        """
        [{'key': 'Content-Type', 'val': 'application/json'},{"key":"TEST","val":"TESTVAL"}]

        {"Content-Type":"application/json"}
        :return str
        """
        if not len(d):
            return ""
        data = {}
        for kv in d:
            data[kv.get("key")] = kv.get('val')
            if "mode" in kv:
                data['mode'] = kv.get('mode')

        return data

    def validate_to_dict(self, d: list) -> list:
        """
         [{"key": "status_code", "val": 200, "mode": "eq"}, {"key": "body.text", "val": "我是棒棒哒图灵机器人", "mode": "eq"},
         {"key": "code", "val": 10000, "mode": "eq"}]

         [{"eq":["status_code",200]}]
        """
        l = []

        for kv in d:
            data = {}
            data[kv['mode']] = [kv.get("key"), kv.get('val')]
            l.append(data)
        return l

    def dict_to_body(self, a: dict):
        data = []
        for k, v in a.items():
            d = dict(key=k, val=v)
            data.append(d)
        return json.dumps(data, ensure_ascii=False)

    def to_dict(self, params: list):
        pass


if __name__ == '__main__':
    d = [{"key": "key", "val": "8fe3b232710c4c0d87b761ed5301e7a4"}, {"key": "info", "val": "今天天气怎么样"},
         {"key": "loc", "val": "北京中关村"}, {"key": "userid", "val": "123456"}]
    b = {"key": "8fe3b232710c4c0d87b761ed5301e7a4", "info": "你叫什么", "userid": "123456"}
    g = [{"key": "status_code", "val": 200, "mode": "eq"}, {"key": "body.text", "val": "我是棒棒哒图灵机器人", "mode": "eq"},
         {"key": "code", "val": 10000, "mode": "eq"}]

    dd = [{'id': 1, 'name': '录入关键词', 'desc': 'desc', 'type': 'id', 'locator': 'kw', 'do': 'send_keys', 'value': 'java'},
          {'id': 2, 'name': '点击确定', 'desc': 'desc', 'type': 'xpath', 'locator': "//input[@id='su']", 'do': 'click'}]
