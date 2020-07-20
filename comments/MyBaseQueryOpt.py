# encoding: utf-8
"""
@auth: cyq
@name: MyBaseQueryOpt
@desc: ModelOPt
"""
from flask_sqlalchemy import BaseQuery


class MyBaseQuery(BaseQuery):
    def filter_by(self, **kwargs):
        """軟刪除"""
        kwargs.setdefault("status", 1)
        return super().filter_by(**kwargs)
