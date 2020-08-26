# -*- coding: utf-8 -*-
# @Author  : cyq
# @File    : Verify.py
# @Desc    : 斷言
import json

from flask import abort

from comments.log import get_log

log = get_log(__name__)


class Verify:

    def __init__(self, step: dict):
        self.step = step
        self.validate = json.loads(self.step['validate'])

        self.resData = self.step['data']
        self.expData = self.validate['expData']
        self.mode = self.validate['mode']

    def verify(self):
        try:
            if self.mode == 'eq':
                return self.resData == self.expData, [self.expData, self.resData]
            elif self.mode == "un_eq":
                return self.resData != self.expData, [self.expData, self.resData]
        except KeyError as e:
            log.exception(e)
            abort(500, f"err:{e}")
