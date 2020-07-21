#!/usr/bin/env python3
# -*- coding:utf-8 -*-
# author:muji
# datetime:2019/8/1 12:01
import os

root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
case_log_path = os.path.join(root_path, 'case_log')
if not os.path.exists(case_log_path):
    os.mkdir(case_log_path)

log_path = os.path.join(root_path, 'log')
if not os.path.exists(log_path):
    os.mkdir(log_path)


class Config:
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@db:3306/dev01'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = 'SFOWS.FSSPWLSD'
    PER_PAGE = 10
    CASE_LOG_PATH = case_log_path
    LOG_PATH = log_path
    LOG_NAME = os.path.join(log_path, 'server.log')


class TestConfig(Config):
    pass


class DevelopConfig(Config):
    pass


class ProdConfig(Config):
    pass


config = ProdConfig
