# encoding: utf-8
"""
@auth: cyq
@name: MyBaseQueryOpt
@desc: 重新封装下BaseQuery
"""

from flask_restful import abort
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
            log.error("id错误或不存在")
            handelAbort("id错误或不存在")
        elif rv.status == 0:
            log.error("id已删除")
            handelAbort("id已删除")
        return rv


def handelAbort(msg):
    abort(dict(code=1, data="", msg=msg))
