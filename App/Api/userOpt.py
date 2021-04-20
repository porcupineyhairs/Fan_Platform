# encoding: utf-8
"""
@auth: cyq
@name: userOpt
@desc: 用户接口
"""

from flask import jsonify, request, g
from flask_restful import Resource, Api

from App import db, auth
from App.Api import v1
from App.Api.errors_and_auth import is_admin
from Model.Models import Part, User
from comments.log import get_log

log = get_log(__file__)


@v1.route("/login", methods=['POST'])
def login():
    username = request.json.get("username", "")
    password = request.json.get('password', "")
    user = User.query.filter(User.username == username).first()
    if user:
        res = user.verify_password(password)
        if res:
            token = user.generate_auth_token(6000)
            return jsonify(dict(code=0, data=token.decode("ascii"),msg="success"))
        else:
            return jsonify(dict(code=1, data="", msg="err password"))
    return jsonify(dict(code=1, data="", msg="null user"))


@v1.route("/getToken", methods=["POST"])
@auth.login_required
def get_auth_token():
    token = g.user.generate_auth_token(600)
    return jsonify(dict(token=token.decode("ascii")))


class NewPart(Resource):
    """增加部門"""

    @auth.login_required
    @is_admin
    def post(self):
        partName = request.json.get('partName')
        if not partName:
            return jsonify(dict(code=1, err="参数错误"))
        try:
            part = Part.query.filter(Part.Part_Name == partName).first()
            if part:
                return jsonify(dict(code=1, err="部门名称存在"))
            new_part = Part(partName=partName)
            new_part.save()
            return jsonify(dict(code=0, data=new_part.id, msg='ok'))
        except Exception as e:
            db.session.rollback()
            log.exception(e)
            return jsonify(dict(code=1, err=f"错误:{str(e)}"))
        finally:
            db.session.close()

    @auth.login_required
    @is_admin
    def get(self):
        """查询部门"""


        try:
            partId = request.args.get("partId")
            if partId:
                part = [Part.get(partId)]
            else:
                part = Part.all()

            data = {
                "code": 0,
                "msg": "ok",
                "data": [{"id": p.id, "status": p.status, "Part_Name": p.Part_Name,
                          "users": [
                              {"uid": i.id, "status": i.status, "name": i.username, 'email': i.email, "phone": i.phone}
                              for i in
                              p.Part_Users.all()]} for p in part]
            }
            return jsonify(data)
        except Exception as e:
            log.exception(str(e))
            return jsonify(dict(code=1, err=str(e)))


# 用户侧删改查
class UserOpt(Resource):
    """注冊"""

    def post(self):
        username = request.json.get("username")
        password = str(request.json.get('password'))
        part_id = request.json.get('partId')
        admin = request.json.get("admin")
        email = request.json.get("email")
        gender = request.json.get('gender')
        phone = request.json.get('phone')
        if not username or not password:  # 必传
            return jsonify(dict(code=1, err="请正确传参"))
        if not email:
            email = username + "@fun.com"

        try:
            # 判斷部門是否存在
            if not Part.query.get(part_id):
                return jsonify(dict(code=1, err=f"portId: {part_id} 错误"))
            # 判斷用户名重复
            if User.query.filter(User.username == username).first():
                return jsonify(dict(code=1, err="姓名重复"))

            user = User(username=username, phone=phone, password=password, email=email, partId=part_id, gender=gender,
                        admin=admin)
            user.save()
            return jsonify(dict(code=0, data=user.id, msg=f"hello {user.username}"))
        except Exception as e:
            log.exception(e)

            return jsonify(dict(err="网络错误", msg=f"{str(e)}"))
        finally:
            db.session.rollback()
            db.session.close()

    @auth.login_required
    @is_admin
    def get(self):
        user_id = request.args.get("id")

        if user_id:
            user = [User.get(user_id)]
            log.info(f"{__name__} userID:{user_id}")
        else:
            log.info(msg=f"{__name__} userID:None")
            user = User.all()
        data = {
            "code": 0,
            "msg": "ok",
            "data": [{"id": i.id, "status": i.status, "name": i.username, "email": i.email, "gender": i.gender,
                      "part": i.part, } for i in user]}
        return jsonify(data)


    @auth.login_required
    @is_admin
    def delete(self):
        id = request.json.get('id')
        if not id:
            return jsonify(dict(code=1, err="id 参数错误"))
        try:
            User.get(id).delete()
            return jsonify(dict(code=0, data="", msg='ok'))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=1, err=f"错误:{str(e)}"))
        finally:
            db.session.close()


api_script = Api(v1)
api_script.add_resource(NewPart, "/partOpt")
api_script.add_resource(UserOpt, '/userOpt')
