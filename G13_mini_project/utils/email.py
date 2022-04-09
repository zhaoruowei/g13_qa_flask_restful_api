# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: email.py
@Time: 2022/3/2911:10
@Software: PyCharm
"""

from flask_mail import Message
import string
import random

from exts import mail


class EmailCaptcha:
    pin_pool = string.ascii_letters + string.digits

    def __init__(self, email_addr):
        self.email_addr = email_addr
        self.pin = self.create_pin()
        self.message = self.create_message()

    def create_message(self):
        message = Message(
            subject="PIN Code",
            recipients=[self.email_addr],
            body=f"Your PIN is: {self.pin}"
        )
        return message

    def send_message(self):
        mail.send(self.message)
        return "Send message success!"

    @classmethod
    def create_pin(cls):
        pin = "".join(random.sample(cls.pin_pool, 4))
        return pin
