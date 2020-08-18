# -*- coding: utf-8 -*-
# @Author  : cyq
# @File    : Verify.py
# @Desc    : 斷言
import json


class Verify:

    def __init__(self, step: dict):
        self.data = {step["variable"]: step['data']}
        self.validate = json.loads(step['validate'])

        print(self.data, self.validate)

    def verify(self):
        for val in self.validate:


