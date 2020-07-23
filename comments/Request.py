# encoding: utf-8
"""
@auth: cyq
@name: Request
@desc: 请求类
"""

import json
import pytest
import requests
from .log import get_log

log = get_log(__name__)


class RequestTool:

    def __init__(self):
        self.res = None

    def requestTool(self, method, url, params, body=None, headers=None):

        if method == "GET":
            try:
                self.res = requests.get(url=url, params=params, headers=headers)
            except Exception as e:
                pytest.fail(str(e), pytrace=False)
                log.info('GetRequestError:', str(e))
        else:
            try:
                self.res = requests.post(url=url, data=json.dumps(body), params=params, headers=headers)
            except Exception as e:
                pytest.fail(str(e), pytrace=False)
                log.info('PostRequestError:', str(e))
        log.info('返回值：%s' % self.res.text)
        return self.res


#
#
if __name__ == '__main__':
    RequestTool().requestTool('', '', '')
