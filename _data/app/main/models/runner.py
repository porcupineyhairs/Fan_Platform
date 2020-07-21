#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/7/22 14:57
import json
import os
from datetime import datetime

import yaml
from httprunner.api import HttpRunner
from werkzeug.utils import secure_filename

from app.errors.exceptions import DatabaseException, RunningTestException
from app.main.models import CaseInfo, ProjectInfo, ModuleInfo
from app.config import config


def run_tests_by_path(time_path):
    """根据目录运行测试用例"""
    runner = HttpRunner(report_dir='report')
    res = runner.run(time_path)
    return runner.summary


# def run_case(id, time_path):
#     path = load_case(id, time_path)
#     if path:
#         return run_tests_by_path(time_path)
#     else:
#         print('用例加载不成功')
#         raise RunningTestException()

def load_case(id, type, time_path):
    if type == 'case':
        return load_case_case(id, time_path)
    elif type == 'module':
        return load_module_case(id, time_path)
    elif type == 'project':
        return load_project_case(id, time_path)


def run_single(id, type):
    """
    运行单个测试用例。
    :param id: int.
    :param type: 项目还是模块还是测试套件还是用例
    :return:
    """
    # 生成 yml 文件
    # 生成时间文件夹
    current_time = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    time_path = os.path.join(config.CASE_LOG_PATH, current_time)
    os.mkdir(time_path)
    try:
        load_case(id, type, time_path)
    except DatabaseException:
        pass
    return run_tests_by_path(time_path)


def run_batch(ids, type):
    """
    批量运行测试用例。
    :param ids: str
    :param type: 项目还是模块还是测试套件还是用例
    :return:
    """
    current_time = datetime.now().strftime('%y-%m-%d-%H-%M-%S')
    time_path = os.path.join(config.CASE_LOG_PATH, current_time)
    os.mkdir(time_path)

    for id in ids.values():
        try:
            load_case(id, type, time_path)
        except DatabaseException:
            pass
    return run_tests_by_path(time_path)


def gen_project_dir(time_path, project_name):
    """创建时间和项目文件夹"""
    project_name_dir = os.path.join(time_path, project_name)
    if not os.path.exists(project_name_dir):
        os.mkdir(project_name_dir)
    return project_name_dir


def load_project_case(id, time_path):
    """根据项目加载用例"""
    project = ProjectInfo.get(int(id))
    if not project:
        raise DatabaseException('没有 module', id)
    modules = project.module_records
    if not modules:
        raise DatabaseException()
    for m in modules:
        load_module_case(m.id, time_path)
    return True


def load_module_case(id, time_path):
    """根据模块加载用例"""
    module = ModuleInfo.get(int(id))
    if not module:
        raise DatabaseException()
    cases = module.case_records
    if not cases:
        raise DatabaseException()
    for c in cases:
        if not load_case_case(c.id, time_path):
            raise RunningTestException
    return True


def load_case_case(case_id, time_path):
    """
    加载单个case用例信息, httprunner, [] ==> yml.loads()
    :param index: int or str：用例索引
    """

    case = CaseInfo().get(int(case_id))
    if not case:
        raise DatabaseException('没有 case ', case_id)

    # TODO: base_url 根据项目和接口拼接
    config = {
        "config": {
            "name": case.name,
            "request": {
                "base_url": None
            }
        }
    }
    case_info = []
    case_info.append(config)

    # 获取用例信息
    # TODO: include 添加
    if case.include:
        include = eval(case.include)
        for pre_case_list in include:
            pre_case = CaseInfo.get(int(pre_case_list[0]))
            request = json.loads(pre_case.request)
            name = pre_case.name

            pre_case = {
                "test": request
            }
            pre_case["test"]["name"] = name
            case_info.append(pre_case)

    # include = eval(case.include)
    request = json.loads(case.request)
    name = case.name
    project = case.module.project
    module = case.module

    the_case = {
        "test": request
    }
    the_case["test"]["name"] = name
    case_info.append(the_case)

    # 生成测试用例的文件夹 gen_case_file()
    project_dir = gen_project_dir(time_path, project.project_name)
    module_dir = os.path.join(project_dir, str(module.id) + module.module_name)
    if not os.path.exists(module_dir):
        os.mkdir(module_dir)
    case_file = os.path.join(module_dir, secure_filename(str(case.id) + name + '.yml'))

    f = open(case_file, 'w', encoding='utf-8')
    yaml.dump(case_info, f)
    return True
