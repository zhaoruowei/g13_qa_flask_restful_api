# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: users.py
@Time: 2022/3/2420:26
@Software: PyCharm
"""

from exts import db
from datetime import datetime
from .base import BaseModel


class UserModel(db.Model, BaseModel):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    join_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email, username, password):
        self.email = email
        self.username = username
        self.password = password

    @classmethod
    def query_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def query_by_username(cls, username):
        return cls.query.filter_by(username=username).first()
