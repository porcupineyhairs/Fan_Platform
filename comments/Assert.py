# encoding: utf-8
"""
@auth: cyq
@name: Request
@desc: 封装Assert方法
"""


import jsonpath
import json
from .log import get_log

class Assertions:
    log = get_log(__name__)

    def assert_code(self, code, expect_code):
        """
        验证response状态码
        :param code:
        :param expect_code:
        :return:
        """
        self.log.info('assert: response code')
        try:
            assert code == expect_code
            return True
        except Exception:
            self.log.info('AssertionError: expect_code is %s, statusCode is %s ' % (expect_code, code))
            raise

    def assert_key_value(self, response_msg, expect_msg):
        """
        验证response response_msg中是否包含期望返回值key-value是否相等或key存在
        :param response_msg:
        :param expect_msg:
        :return:
        """
        self.log.info('assert: response key_value')
        try:
            if isinstance(expect_msg, dict):
                for key in expect_msg.keys():
                    assert key in response_msg
                    if isinstance(expect_msg[key], list):
                        for i in range(len(expect_msg[key])):
                            self.assert_key_value(response_msg[key][i], expect_msg[key][i])
                    elif isinstance(expect_msg[key], dict):
                        self.assert_key_value(response_msg[key], expect_msg[key])
                    elif expect_msg[key] != None:
                        assert expect_msg[key] == response_msg[key]
            elif isinstance(expect_msg, list):
                for i in range(len(expect_msg)):
                    self.assert_key_value(response_msg[i], expect_msg[i])
            else:
                assert response_msg == expect_msg

            return True
        except Exception:
            self.log.info("AssertionError: expect_key is %s \n responseText is %s" % (expect_msg, response_msg))
            raise

    def assert_jsonpath(self, response_msg, expect_msg, jsonpath_msg):
        """
        通过jsonpath校验返回值是否符合期望值
        :param response_msg:
        :param expect_msg:
        :param jsonpath_msg:
        :return:
        """
        try:
            if jsonpath_msg:
                self.log.info('assert: jsonpath %s' % json.dumps(jsonpath_msg))
                for i in jsonpath_msg:
                    # 获取jsonpath参数的数值
                    method = i['method']
                    json_path = i['json_path']
                    jsonpath_list = jsonpath.jsonpath(response_msg, json_path)
                    self.log.info('assert: json_data = %s' % jsonpath_list)
                    self.log.info('assert: method = %s' % method)

                    # 处理期望值中的jsonpath
                    if '$' in str(i['expect_value']):
                        expect_value = jsonpath.jsonpath(response_msg, i['expect_value'])[0]
                    else:
                        expect_value = i['expect_value']
                    self.log.info('assert: expect_value = %s' % expect_value)

                    # 对jsonpath的值作判断
                    if jsonpath_list is not False:
                        # 长度方法判断
                        if 'length' in method:
                            # 计算嵌套列表的元素个数
                            list_len = 0
                            for item in jsonpath_list:
                                if isinstance(item, list):
                                    list_len += len(item)
                            list_len += len(jsonpath_list)
                            self.log.info('assert: length_value = %s' % list_len)

                            if '==' in method:
                                assert list_len == expect_value
                            elif '>=' in method:
                                assert list_len >= expect_value
                        # 常规方法判断
                        else:
                            for json_value in jsonpath_list:
                                if method == 'in':
                                    assert (expect_value in jsonpath_list) or (expect_value in json_value)
                                elif method == 'notin':
                                    assert expect_value not in json_value or expect_value not in jsonpath_list
                                elif method == '==':
                                    assert json_value == expect_value
                                elif method == '<=':
                                    assert json_value <= expect_value
                                elif method == '>=':
                                    assert json_value >= expect_value
                                elif method == 'haskey':
                                    assert expect_value in json_value.keys()
                                elif method == 'nokey':
                                    assert expect_value not in json_value.keys()
                                elif method == '!=':
                                    assert json_value != expect_value
                    else:
                        self.log.info("JsonpathError: jsonpath value is False, please check it")
                       # raise

            return True
        except Exception:
            self.log.info("JsonpathError: jsonpath function failed, please check it")
            raise
