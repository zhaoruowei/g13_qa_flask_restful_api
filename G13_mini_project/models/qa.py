# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: qa.py
@Time: 2022/3/3123:15
@Software: PyCharm
"""

from exts import db
from datetime import datetime
from .base import BaseModel


class QuestionModel(db.Model, BaseModel):
    __tablename__ = "question"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    post_time = db.Column(db.DateTime, default=datetime.now)

    author = db.relationship("UserModel", backref="questions")

    def __init__(self, title, content, author_id):
        self.title = title
        self.content = content
        self.author_id = author_id


class AnswerModel(db.Model, BaseModel):
    __tablename__ = "answer"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    question_id = db.Column(db.Integer, db.ForeignKey("question.id"))
    create_time = db.Column(db.DateTime, default=datetime.now)

    author = db.relationship("UserModel", backref="answers")
    question = db.relationship("QuestionModel", backref=db.backref("answers", order_by=create_time.desc()))

    def __init__(self, content, author_id, question_id):
        self.author_id = author_id
        self.content = content
        self.question_id = question_id
