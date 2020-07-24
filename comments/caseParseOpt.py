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
        return data

    def dict_to_body(self, a: dict):

        data = []
        for k, v in a.items():
            d = dict(key=k, val=v)
            data.append(d)
        return data


if __name__ == '__main__':
    d = [{"key": "key", "val": "8fe3b232710c4c0d87b761ed5301e7a4"}, {"key": "info", "val": "今天天气怎么样"},
         {"key": "loc", "val": "北京中关村"}, {"key": "userid", "val": "123456"}]
    b = {'key': '8fe3b232710c4c0d87b761ed5301e7a4', 'info': '今天天气怎么样', 'loc': '北京中关村', 'userid': '123456'}

    CaseParseOpt().body_to_dict(d)
    CaseParseOpt().dict_to_body(b)
