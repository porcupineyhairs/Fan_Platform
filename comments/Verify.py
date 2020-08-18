# -*- coding: utf-8 -*-
# @Author  : cyq
# @File    : Verify.py
# @Desc    : 斷言
import json


class Verify:

    def __init__(self, step: dict):
        self.step = step
        self.resData = self.step['data']
        self.expData = json.loads(self.step['validate'])
        self.mode = self.expData.pop("mode")

    def verify(self):
        if self.mode == 'eq':
            return self.resData == self.expData['expData']
