# encoding: utf-8
"""
@auth: cyq
@name: init_data
@desc: 生成假数据
"""
import random

from faker import Faker

from App import create_app
from Model.Models import *

f = Faker(locale="zh_CN")


def add_project(nums: int):
    """增加测试项目"""
    create_app().app_context().push()

    for i in range(nums):
        p = Project(name=f"{f.company()}", desc=f"{f.word()}")
        db.session.add(p)
    db.session.commit()
    print('ok')


def add_user(nums: int, superUser: bool = False):
    """
    增加测试用户
    """
    create_app().app_context().push()
    if superUser:
        u = User(username="cyq", password="cyq", email=f.email(), phone=f.phone_number(), partId=1,
                 admin=True, gender=random.choice([True, False]))
        db.session.add(u)
        db.session.commit()
    else:
        for i in range(nums):
            u = User(username=f.name(), password=f.pystr(), email=f.email(), phone=f.phone_number(), partId=1,
                     admin=random.choice([True, False]), gender=random.choice([True, False]))

            db.session.add(u)
        db.session.commit()


def add_part(nums: int):
    """
    增加测试部门
    """
    create_app().app_context().push()

    for i in range(nums):
        p = Part(partName=f.job())
        db.session.add(p)
    db.session.commit()


def add_Interface(nums: int):
    """增加接口"""

    create_app().app_context().push()

    for i in range(nums):
        p = Interfaces(name=f.job(), desc=f.pystr(), pid=1)
        db.session.add(p)
    db.session.commit()


def add_Case():
    create_app().app_context().push()

    Case(name="图灵", request="test").save()


if __name__ == '__main__':
    add_Case()
