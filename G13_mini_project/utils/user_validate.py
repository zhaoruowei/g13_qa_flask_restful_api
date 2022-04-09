# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: user_validate.py
@Time: 2022/4/218:23
@Software: PyCharm
"""

from models.email import EmailCaptchaModel
from models.users import UserModel


def validate_captcha(email, captcha):
    captcha_model = EmailCaptchaModel.query_by_email(email)
    if not captcha_model or captcha_model.captcha != captcha:
        return 0
    return 1


def validate_email(email):
    user_model = UserModel.query_by_email(email)
    if user_model:
        return 0
    return 1


def validate_username(username):
    user_model = UserModel.query_by_username(username)
    if user_model:
        return 0
    return 1
