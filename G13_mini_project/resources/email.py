# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: email.py
@Time: 2022/3/2421:19
@Software: PyCharm
"""

from flask_restful import Resource, reqparse

from models.email import EmailCaptchaModel
from utils.email import EmailCaptcha

parser = reqparse.RequestParser()
parser.add_argument('email', type=str, required=True, help="Email cannot be blank.", location=["form"])


class Email(Resource):
    email_parser = parser.copy()

    def post(self):
        args = Email.email_parser.parse_args(strict=True)
        email_addr = args["email"]

        if email_addr == "":
            return {"code": 400, "message": "Email cannot be blank!"}, 400

        email_obj = EmailCaptcha(email_addr)

        captcha_model = EmailCaptchaModel.query_by_email(email_obj.email_addr)
        if captcha_model:
            captcha_model.update_to_db(email_obj.email_addr, email_obj.pin)
        else:
            captcha_model = EmailCaptchaModel(email_obj.email_addr, email_obj.pin)
            captcha_model.insert_to_db()

        email_obj.create_message()
        email_obj.send_message()

        return {"code": 200, "message": "Get success!"}, 200

