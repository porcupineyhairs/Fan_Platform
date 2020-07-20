# encoding: utf-8
"""
@auth: cyq
@name: UniqueOpt
@desc: 验证
"""
from wtforms import ValidationError


class Unique:

    def __init__(self, db_class, db_column, msg=None):
        self.db_class = db_class
        self.db_column = db_column
        self.msg = "数据已存在" if msg is None else msg

    def __call__(self, form, field):
        res = self.db_class.query.filter(self.db_column == field.data).first()

        if res:
            raise ValidationError(self.msg)

        return res
