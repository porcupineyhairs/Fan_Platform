# encoding: utf-8
"""
@auth: cyq
@file: view.py
@desc: 接口用例函数
"""
import json
import os


def generate_case_files(instance, env, case_dir_path):
    cases_list = []
    config = {
        'config': {
            'name': instance.name,
            'request': {
                'base_url': env.base_url if env else ''
            }
        }
    }
    cases_list.append(config)

    # 获取当前用例的前置配置和前置用例
    include = json.loads(instance.include, encoding='utf-8')

    # 获取当前用例的请求信息
    request = json.loads(instance.request, encoding='utf-8')

    # 接口名称
    interface_name = instance.interface.name
    # 项目名称
    project_name = instance.project.name

    case_dir_path = os.path.join(case_dir_path,project_name)
    # 判断时候存在

    if not os.path.exists(case_dir_path):
        os.makedirs(case_dir_path)
