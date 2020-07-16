from flask import jsonify
from flask_restful import Resource, Api
from App.Api import v1

class Index(Resource):

    def get(self):
        return jsonify(dict(msg="index"))


api = Api(v1)
api.add_resource(Index, '/')
