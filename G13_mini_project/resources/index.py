# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: index.py
@Time: 2022/3/2421:39
@Software: PyCharm
"""

from flask_restful import Resource, marshal, fields

from models.qa import QuestionModel

question_fields = {
    "uid": fields.Integer(attribute="id"),
    "author": fields.String(attribute="author.username"),
    "time": fields.DateTime(attribute="post_time"),
    "title": fields.String(attribute="title"),
    "content": fields.String(attribute="content")
}


class Index(Resource):
    def get(self):
        questions = QuestionModel.query.order_by("post_time").all()
        data = marshal(questions, question_fields)
        if len(data) != 0:
            return {"code": 200, "message": "Get success!", "question": marshal(questions, question_fields)}, 200
        else:
            return {"code": 200, "message": "Get success!", "question": "None data!"}, 200

