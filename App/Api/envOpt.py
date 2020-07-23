# encoding: utf-8
"""
@auth: cyq
@file: envOpt.py
@desc: 测试环境
"""
from flask import request, jsonify
from flask_restful import Api, Resource

from Model.Models import Envs
from comments.log import get_log
from . import v1
from .errors_and_auth import is_admin
from .. import auth, db

log = get_log(__name__)


class EnvOpt(Resource):

    @auth.login_required
    @is_admin
    def post(self):
        name = request.json.get("name")
        url = request.json.get('url')
        desc = request.json.get('desc')
        if not name or not url:
            return jsonify(dict(code=1, data="", err="缺少必传参数"))
        try:
            # 判断url:
            e = Envs.query.filter(Envs.base_url == url).first()
            if e:
                return jsonify(dict(code=1, data="", err="url重复"))
            e = Envs(name=name, url=url, desc=desc)
            e.save()
            return jsonify(dict(code=0, data=f"{e.id}", msg="ok"))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, data="", msg="错误"))

        finally:
            db.session.close()

    @auth.login_required
    @is_admin
    def put(self):
        id = request.json.get("id")
        url = request.json.get('url')
        desc = request.json.get('desc')
        if not id:
            return jsonify(dict(code=1, err="缺少必传参数"))
        try:
            e = Envs.get(id)
            if Envs.query.filter(Envs.base_url == url).first():
                return jsonify(dict(code=1, data="", err="url重复"))
            e.base_url = url
            e.desc = desc
            e.save()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=0, err=f"{e}"))

    def get(self):
        try:
            e = Envs.all()
            data = {
                "code": 0,
                "msg": "ok",
                "data": [
                    {"id": i.id, "name": i.name, "base_url": i.base_url, "desc": i.desc}
                    for i in e],
                "total": len(e)
            }
            return jsonify(data)
        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=1, data="", err=f"错误:{str(e)}"))

    @auth.login_required
    @is_admin
    def delete(self):
        id = request.json.get("id")
        if not id:
            return jsonify(dict(code=1, err="缺少必传参数"))
        try:
            e = Envs.get(id)
            e.delete()
            return jsonify(dict(code=0, data="", msg="ok"))
        except Exception as e:
            log.exception(e)
            return jsonify(dict(code=0, err=f"{e}"))


api_script = Api(v1)
api_script.add_resource(EnvOpt, "/envOpt")
