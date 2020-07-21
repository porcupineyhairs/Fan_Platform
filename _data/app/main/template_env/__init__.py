#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/5 14:38
import json
from datetime import datetime


def str_time(ts):
    return datetime.fromtimestamp(ts)

def json_loads(my_str):
    try:
        return json.loads(my_str)
    except ValueError:
        return my_str

# def add_global():
#     def json_loads(my_str):
#         try:
#             return json.loads(my_str)
#         except ValueError:
#             return my_str
#     return dict(json_loads=json_loads)
