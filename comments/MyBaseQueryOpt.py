# encoding: utf-8
"""
@auth: cyq
@name: MyBaseQueryOpt
@desc: 重新封装下BaseQuery
"""

from flask import abort
# from flask_restful import abort
from flask_sqlalchemy import BaseQuery

from .log import get_log

log = get_log(__name__)


class MyBaseQuery(BaseQuery):

    def filter_by(self, **kwargs):
        """过滤軟刪除"""
        kwargs.setdefault("status", 1)
        return super().filter_by(**kwargs)

    def get_or_NoFound(self, ident):
        rv = self.get(ident)
        if not rv:
            err_msg = "id错误或不存在"
            abort(400, err_msg)
        elif rv.status == 0:
            err_msg = 'id已删除'
            abort(400, err_msg)
        return rv
