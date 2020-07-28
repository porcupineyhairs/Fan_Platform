# encoding: utf-8
"""
@auth: cyq
@name: Request
@desc: 请求类
"""
import json

import requests
from requests import exceptions

from .log import get_log

log = get_log(__name__)


class DelCase:
    """
         [{'stepName': '请求',
     'stepDesc': 'step_desc',
      'stepUrl': 'http://www.tuling123.com/openapi/api',
       'stepMethod': 'POST',
        'stepHeaders': {'Content-Type': 'application/json'},
         'stepBody': {'key': '8fe3b232710c4c0d87b761ed5301e7a4', 'info': '今天天气怎么样', 'loc': '北京中关村', 'userid': '123456'}, 'stepRequest': '', 'stepResponse': {'code': 100000, 'text': '请问你想查询哪个城市'},
          'stepJsonpath': '',
           'stepExtract': ''}]
    """

    def __init__(self, caseInfo: str):
        self.case = json.loads(caseInfo)

    def run(self):
        for i in self.case:
            resp = Req(url=i['stepUrl'], method=i['stepMethod'].lower(), headers=i['stepHeaders'],
                       req=i['stepBody']).testApi()
            print(resp)


class Req:
    def __init__(self, url, method, headers, req):
        self.url = url
        self.method = method
        self.headers = headers
        self.req = req
        self.resp = []
        print(f"url     =====  {url}")
        print(f"method  =====  {method}")
        print(f"headers =====  {headers}")
        print(f"req     =====  {req}")

    def testApi(self):
        if self.method == "get":
            try:
                self.r = requests.get(url=self.url, headers=self.headers, params=self.req, timeout=100)
                self.r.encoding = 'UTF-8'
                spend = self.r.elapsed.total_seconds()
                json_response = json.loads(self.r.text)
                return json_response, spend
            except exceptions.Timeout as e:
                log.exception(e)
                return {'get请求出错': "请求超时"}
            except exceptions.InvalidURL as e:
                log.exception(e)
                return {'get请求出错': "非法url"}
            except exceptions.HTTPError as e:
                log.exception(e)
                return {'get请求出错': "http请求错误"}
            except Exception as e:
                log.exception(e)
                return {'get请求出错': "错误原因:%s" % e}

        elif self.method == "post":
            try:
                self.r = requests.post(url=self.url, headers=self.headers,
                                       data=json.dumps(self.req), timeout=100)
                json_response = json.loads(self.r.text)
                spend = self.r.elapsed.total_seconds()
                return json_response, spend
            except exceptions.Timeout as e:
                log.exception(e)
                return {'get请求出错': "请求超时"}
            except exceptions.InvalidURL as e:
                log.exception(e)
                return {'get请求出错': "非法url"}
            except exceptions.HTTPError as e:
                log.exception(e)
                return {'get请求出错': "http请求错误"}
            except Exception as e:
                log.exception(e)
                return {'get请求出错': "错误原因:%s" % e}
