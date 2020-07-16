# encoding: utf-8
"""
@auth: cyq
@name: userOpt
@desc: 用户接口
"""
import os

from flask import jsonify, request, g
from flask_restful import Resource, Api
from App import auth,catch
from App.Api import v1
from App.Api.errors_and_auth import InvalidUsage, is_admin


class Index(Resource):

    @auth.login_required
    @is_admin
    def get(self):
        print(auth.username())
        data =[i for i in range(10)]
        print(data[0])
        return jsonify(dict(msg="index",data=data))


@v1.route('/err')
def get_foo():
    raise InvalidUsage("errrr", status_code=500)




api = Api(v1)
api.add_resource(Index, '/')

