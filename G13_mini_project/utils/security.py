# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: security.py
@Time: 2022/3/250:29
@Software: PyCharm
"""

from werkzeug.security import generate_password_hash, check_password_hash


def password_hash(password):
    h_password = generate_password_hash(password)
    return h_password


def password_hash_check(password, h_password):
    return True if check_password_hash(h_password, password) else False
