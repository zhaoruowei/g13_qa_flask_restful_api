# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: config.py
@Time: 2022/3/2317:22
@Software: PyCharm
"""

import os


class DefaultConfig(object):
    # flask configure
    # security using os.urandom method generate random characters
    key_size = 24
    SECRET_KEY = os.urandom(key_size)

    # database configure
    HOSTNAME = "127.0.0.1"
    PORT = "3306"
    DATABASE = "myapp"
    USERNAME = "username"
    PASSWORD = "password"
    DB_URI = "mysql+pymysql://{}:{}@{}:{}/{}".format(USERNAME, PASSWORD, HOSTNAME, PORT, DATABASE)
    # sqlalchemy configure
    SQLALCHEMY_DATABASE_URI = DB_URI
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # for chinese output
    JSON_AS_ASCII = False

    # debug
    DEBUG = True

    # flask mail
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 465
    MAIL_USE_TLS = False
    MAIL_USE_SSL = True
    MAIL_DEBUG = True
    MAIL_USERNAME = "username"
    MAIL_PASSWORD = "password"
    MAIL_DEFAULT_SENDER = "username"
    pass


class DevelopmentConfig(DefaultConfig):
    pass


class ProductionConfig(DefaultConfig):
    pass
