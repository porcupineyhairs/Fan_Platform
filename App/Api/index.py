# encoding: utf-8
"""
@auth: cyq
@name: userOpt
@desc: 用户接口
"""

from flask_restful import Resource, Api

from App.Api import v1

class Index(Resource):

    def get(self):
        print('index')
        return "ok"


@v1.route("/testUrl", endpoint='testfunc')
def get_foo():
    # raise InvalidUsage("errrr", status_code=500)
    return "ok"



api = Api(v1)
api.add_resource(Index, '/')
