#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 16:04
from run import app
from app.main.models import ProjectInfo, db


def insert_project(num):
    """插入数据库数据"""
    with app.app_context() as ctx:
        for i in range(num):
            project = ProjectInfo(project_name=f'Project {i}')
            db.session.add(project)
        db.session.commit()


def update_project(id):
    with app.app_context() as ctx:
        project = ProjectInfo.query.get(id)
        project.project_name = 'project_oooo'
        db.session.add(project)
        db.session.commit()


if __name__ == '__main__':
    insert_project(11)
