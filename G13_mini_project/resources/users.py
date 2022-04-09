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

from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from models.users import UserModel
from utils.security import password_hash, check_password_hash
from utils.user_validate import validate_email, validate_captcha, validate_username

parser = reqparse.RequestParser()
parser.add_argument("email", type=str, required=True, help="Email cannot be empty!", location=["form"])
parser.add_argument("password", type=str, required=True, help="Password cannot be empty!", location=["form"])
parser.add_argument("captcha", type=str, required=True, help="Captcha cannot be empty!", location=["form"])
parser.add_argument("username", type=str, required=True, help="Username cannot be empty!", location=["form"])
parser.add_argument("confirm_password", type=str, required=True, help="Confirm Password must equal to Password!",
                    location=["form"])


class UserLogin(Resource):
    login_parser = parser.copy()
    login_parser.remove_argument("captcha")
    login_parser.remove_argument("username")
    login_parser.remove_argument("confirm_password")

    def post(self):
        args = UserLogin.login_parser.parse_args(strict=True)
        email = args["email"]
        password = args["password"]

        user = UserModel.query_by_email(email)
        if not user:
            return {"code": 401, "message": "E-mail error!"}, 401

        if not check_password_hash(user.password, password):
            return {"code": 401, "message": "Password error!"}, 401

        access_token = create_access_token(identity={"user_id": f"{user.id}", "username": f"{user.username}"})
        return {"code": 200, "message": "login success!", "access_token": access_token}, 200


class UserRegister(Resource):
    register_parser = parser.copy()

    def post(self):
        args = UserRegister.register_parser.parse_args(strict=True)
        email = args["email"]
        captcha = args["captcha"]
        username = args["username"]
        password = args["password"]
        confirm_password = args["confirm_password"]

        if password != confirm_password:
            return {"code": 400, "message": "Confirm Password must equal to Password!"}, 400

        if not validate_username(username):
            return {"code": 400, "message": "Username has been exists!"}, 400

        if not validate_email(email):
            return {"code": 400, "message": "Email has been exists!"}, 400

        if not validate_captcha(email, captcha):
            return {"code": 400, "message": "Captcha error!"}, 400

        h_password = password_hash(password)
        user = UserModel(email=email, username=username, password=h_password)
        user.insert_to_db()

        return {"code": 201, "message": "User create successfully!"}, 201
