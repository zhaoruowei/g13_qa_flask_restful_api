# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: app.py
@Time: 2022/3/2317:22
@Software: PyCharm
"""

from flask import Flask
from flask_restful import Api

from config import DevelopmentConfig
from exts import db, mail, migrate, cors, jwt
from resources.users import UserLogin
from resources.users import UserRegister
from resources.email import Email
from resources.index import Index
from resources.qaquestion import QAQuestion, QuestionDetail, QAAnswer, QASearch, AnswerDetail

app = Flask(__name__)
app.config.from_object(DevelopmentConfig)
app.config.from_envvar("PROJECT_CONFIG", silent=False)

# initial database
db.init_app(app)

# initial mail
mail.init_app(app)

# initial migrate
migrate.init_app(app, db)

# CORS solution
cors.init_app(app, resource={r"/api/*": {"origins": "*"}})

# JWT
jwt.init_app(app)

api = Api(app)


api.add_resource(UserLogin, "/login")
api.add_resource(UserRegister, "/register")
api.add_resource(Email, "/user/captcha")
api.add_resource(QAQuestion, "/question/public")
api.add_resource(QuestionDetail, "/question/<int:question_id>")
api.add_resource(AnswerDetail, "/answer/<int:answer_id>")
api.add_resource(QAAnswer, "/question/answer")
api.add_resource(QASearch, "/question/search")
api.add_resource(Index, "/")


if __name__ == '__main__':
    app.run(debug=True)
