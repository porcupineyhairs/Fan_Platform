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


@v1.route("/getToken")
@auth.login_required
def get_auth_token():
    try:
        token = g.user.generate_auth_token(600)
        return jsonify(dict(token=token.decode("ascii")))
    except Exception as e:
        log.exception(e)


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
            db.session.add(new_part)
            db.session.commit()
            return jsonify(dict(code=0, msg='ok'))
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
                part = Part.quert.get(partId)
                if not part:
                    return jsonify(dict(code=1, err=f"partId:{partId} 错误或不存在"))
                part = [part]
            else:
                part = Part.query.all()

            data = {
                "code": 0,
                "parts": [{"id": p.id, "Part_Name": p.Part_Name,
                           "users": [{"uid": i.id, "name": i.username, 'email': i.email, "phone": i.phone} for i in
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
            return jsonify(dict(code=0, uid=user.id, msg=f"hello {user.username}"))
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
        try:
            if user_id:
                user = User.query.get(user_id)
                if not user:
                    return jsonify(dict(code=1, err="id錯誤或不存在"))
                user = [user]
            else:
                user = User.query.all()

            data = {
                "code": 0,
                "user": [{"id": i.id, "name": i.username, "email": i.email, "gender": i.gender, "part": i.part} for i
                         in user]
            }
            return jsonify(data)
        except Exception as e:
            db.session.rollback()
            log.exception(str(e))
            return jsonify(dict(code=1, err=f"错误:{str(e)}"))

    @auth.login_required
    @is_admin
    def delete(self):
        id = request.json.get('id')
        if not id:
            return jsonify(dict(code=1, err="id 参数错误"))
        try:
            user = User.query.get(id)
            db.session.delete(user)
            db.session.commit()
            return jsonify(dict(code=0, msg='ok'))
        except Exception as e:
            log.exception(e)
            db.session.rollback()
            return jsonify(dict(code=1, err=f"错误:{str(e)}"))
        finally:
            db.session.close()


@v1.route('/addUsers')
def addUsers():
    """增加测试用户"""
    from faker import Faker
    f = Faker(locale="zh_CN")

    users = [User(username=f.name(), password=f.pystr(), partId=1,phone=f.phone_number(), email=f.email()) for i in range(10)]
    db.session.add_all(users)
    db.session.commit()
    return 'ok'


api_script = Api(v1)
api_script.add_resource(NewPart, "/partOpt")
api_script.add_resource(UserOpt, '/userOpt')
