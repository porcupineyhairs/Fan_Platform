#!/usr/bin/env python3
#-*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/5 15:01
import json

from wtforms import ValidationError

from app.main.models import CaseInfo


class Unique:
    """验证在数据库是否唯一"""

    def __init__(self, db_class, db_column, msg=None):
        self.db_class = db_class
        self.db_column = db_column
        if msg is None:
            msg = '该数据在数据库中已存在'
        self.msg = msg

    def __call__(self, form, filed):
        not_unique = self.db_class.query.filter(self.db_column == filed.data).first()
        if not_unique:
            raise ValidationError(self.msg)
        return filed.data


class Exist:
    """验证在数据库是否存在"""

    def __init__(self, db_class, db_column, msg=None):
        self.db_class = db_class
        self.db_column = db_column
        if msg is None:
            msg = '不存在'
        self.msg = msg

    def __call__(self, form, filed):
        exist = self.db_class.query.filter(self.db_column == filed.data).first()
        if not exist:
            raise ValidationError(self.msg)
        return exist


class RequestData:
    """测试数据验证"""

    def __init__(self, msg=None):
        if msg is None:
            msg = '请求参数不正确'
        self.msg = msg

    def __call__(self, form, filed):
        if not filed.data:
            return filed.data
        if not isinstance(filed.data, dict):
            raise ValidationError(self.msg)

        data = filed.data.get('test')
        if not isinstance(data, list):
            raise ValidationError(self.msg)
        return data

# class ValidateRequestData(RequestData):
#     """验证器"""
#     def __call__(self, form, field):
#         res = super().__call__(form, field)
#         if not res:
#             return res



class IncludeCaseValidate:
    """包含的用例验证器"""

    def __init__(self, msg=None):
        if msg is None:
            msg = '包含的用例不正确'
        self.msg = msg

    def __call__(self, form, filed):
        if not filed.data:
            return []
        cases = filed.data
        cases = cases.replace("'", '"')
        try:
            cases=json.loads(cases)
        except ValueError:
            raise ValidationError(self.msg)
        for case in cases:
            exist = CaseInfo.query.get(int(case[0]))
            if not exist:
                raise ValidationError(self.msg)
        return filed.data


class Choose(object):
    def __init__(self, choices=(), msg=None):
        if msg is None:
            msg = '不在选择范围内'
        self.msg = msg
        self.choices= choices

    def __call__(self, form, field):
        if field.data not in self.choices:
            raise ValidationError(self.msg)
        return field.data