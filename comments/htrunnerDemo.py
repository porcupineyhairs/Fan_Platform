import json
import os

from httprunner import HttpRunner, Config, Step, RunRequest


# class TestCaseRequestWithFunctions(HttpRunner):
#     config = (
#         Config("request methods testcase with functions")
#             .base_url("http://www.tuling123.com/openapi/api")
#             .verify(False)
#     )
#
#     teststeps = [
#         Step(
#             RunRequest("post form data")
#                 # .with_variables(**{"foo2": "bar23"})
#                 .post("http://www.tuling123.com/openapi/api")
#                 .with_headers(
#                 **{"Content-Type": "application/json"}
#             ).with_json(
#                 {"key": "8fe3b232710c4c0d87b761ed5301e7a4", "info": "今天天气怎么样", "loc": "北京中关村", "userid": "123456"})
#
#                 .validate()
#                 .assert_equal("status_code", 200)
#                 .assert_equal("body.code", 100000)
#                 .assert_equal("body.text", "请问你想查询哪个城市")
#             # .assert_equal("body.form.foo3", "bar21")
#         ),
#     ]
#
#
# if __name__ == "__main__":
#     TestCaseRequestWithFunctions().test_start[kv.get("key"),kv.get('val')]()
from suite.pwd import get_cwd
path = get_cwd("图灵14.yml")
print( os.path.splitext(path))
HttpRunner().run_path(path)

