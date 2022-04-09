# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: email.py
@Time: 2022/3/2420:01
@Software: PyCharm
"""

from exts import db
from datetime import datetime
from .base import BaseModel


class EmailCaptchaModel(db.Model, BaseModel):
    __tablename__ = "email_captcha"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    captcha = db.Column(db.String(10), nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)

    def __init__(self, email_addr, captcha):
        self.email = email_addr
        self.captcha = captcha

    @classmethod
    def update_to_db(cls, email_addr, new_captcha):
        cls.query.filter(cls.email == email_addr).update({"captcha": new_captcha, "create_time": datetime.now()})
        db.session.commit()
        pass

    @classmethod
    def query_by_email(cls, email_addr):
        return cls.query.filter_by(email=email_addr).first()
