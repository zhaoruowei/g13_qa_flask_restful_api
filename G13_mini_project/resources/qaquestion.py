# !/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@Author: Feiye Pan, Ruowei Zhao, Tianbao Zhang, Yuting Ma
@Student number: 210038293, 210464838, 210177293, 210568963
@Email: r.zhao@se21.qmul.ac.uk
@Project: G13_Q&A_Platform
@File: qaquestion.py
@Time: 2022/3/3122:25
@Software: PyCharm
"""

from flask_restful import Resource, reqparse, marshal_with, fields, marshal
from flask_jwt_extended import jwt_required, get_jwt_identity
from sqlalchemy import or_
from datetime import datetime

from models.qa import QuestionModel, AnswerModel

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="Title cannot be empty!", location=["form"])
parser.add_argument("content", type=str, required=True, help="Content cannot be empty!", location=["form"])
parser.add_argument("search_key", type=str, required=True, help="Search key cannot be empty!")

question_field = {
    "qid": fields.Integer(attribute="id"),
    "title": fields.String(),
    "content": fields.String(),
    "author": fields.String(attribute="author.username"),
    "time": fields.DateTime(attribute="post_time")
}

answer_field = {
    "qid": fields.Integer(attribute="question.id"),
    "aid": fields.Integer(attribute="id"),
    "content": fields.String(),
    "author": fields.String(attribute="author.username"),
    "time": fields.DateTime(attribute="create_time")
}


class QAQuestion(Resource):
    question_parser = parser.copy()
    question_parser.remove_argument("search_key")

    @jwt_required()
    def post(self):
        args = QAQuestion.question_parser.parse_args(strict=True)
        title = args["title"]
        content = args["content"]
        user_id = int(get_jwt_identity()["user_id"])
        if not title:
            return {"code": 400, "message": "title cannot be empty!"}, 400

        if not content:
            return {"code": 400, "message": "content cannot be empty!"}, 400

        question = QuestionModel(title, content, user_id)
        question.insert_to_db()
        return {"code": 201, "message": "post success!"}, 201


class QuestionDetail(Resource):
    question_put_parser = parser.copy()
    question_put_parser.remove_argument("search_key")
    question_put_parser.replace_argument("title", type=str, required=False, location=["form"])
    question_put_parser.replace_argument("content", type=str, required=False, location=["form"])

    @jwt_required()
    def get(self, question_id):
        question = QuestionModel.query.get_or_404(question_id)

        data = marshal(question, question_field)
        answers = AnswerModel.query.filter_by(question_id=question_id).all()
        data["answers"] = marshal(answers, answer_field)
        return {"code": 200, "message": "Get success", "data": data}, 200

    @jwt_required()
    def put(self, question_id):
        question = QuestionModel.query.get_or_404(question_id)

        user_id = int(get_jwt_identity()["user_id"])
        if user_id != question.author_id:
            return {"code": 403, "message": "No permission"}, 403

        args = QuestionDetail.question_put_parser.parse_args(strict=True)
        title = args["title"]
        content = args["content"]
        time = datetime.now()
        if title:
            question.title = title

        if content:
            question.content = content

        question.post_time = time
        question.insert_to_db()
        return {"code": 200, "message": "PUT success!", "question": marshal(question, question_field)}, 200

    @jwt_required()
    def delete(self, question_id):
        question = QuestionModel.query.get_or_404(question_id)

        user_id = int(get_jwt_identity()["user_id"])
        if user_id != question.author_id:
            return {"code": 403, "message": "No permission"}, 403

        answers = AnswerModel.query.filter_by(question_id=question_id).all()
        if answers:
            for answer in answers:
                answer.delete_from_db()

        question.delete_from_db()
        return {"code": 204, "message": "Delete Success!"}, 204


class QAAnswer(Resource):
    answer_parser = parser.copy()
    answer_parser.remove_argument("title")
    answer_parser.remove_argument("search_key")
    answer_parser.add_argument("question_id", type=int, required=True, help="question_id cannot be empty!")

    @jwt_required()
    def post(self):
        args = QAAnswer.answer_parser.parse_args(strict=True)
        content = args["content"]
        question_id = args["question_id"]
        user_id = int(get_jwt_identity()["user_id"])

        if not content:
            return {"code": 400, "message": "content cannot be empty!"}, 400
        if not question_id:
            return {"code": 400, "message": "question_id cannot be empty!"}, 400

        QuestionModel.query.get_or_404(question_id)

        answer = AnswerModel(content, user_id, question_id)
        answer.insert_to_db()
        return {"code": 201, "message": "post success!"}, 201


class AnswerDetail(Resource):
    answer_put_parser = parser.copy()
    answer_put_parser.remove_argument("search_key")
    answer_put_parser.remove_argument("title")
    answer_put_parser.replace_argument("content", type=str, required=False, location=["form"])

    @jwt_required()
    def put(self, answer_id):
        answer = AnswerModel.query.get_or_404(answer_id)

        user_id = int(get_jwt_identity()["user_id"])
        if user_id != answer.author_id:
            return {"code": 403, "message": "No permission!"}, 403

        args = AnswerDetail.answer_put_parser.parse_args(strict=True)
        content = args["content"]
        time = datetime.now()

        if content:
            answer.content = content

        answer.content_time = time
        answer.insert_to_db()
        return {"code": 200, "message": "PUT success!", "answer": marshal(answer, answer_field)}, 200

    @jwt_required()
    def delete(self, answer_id):
        answer = AnswerModel.query.get_or_404(answer_id)

        user_id = int(get_jwt_identity()["user_id"])
        if user_id != answer.author_id:
            return {"code": 403, "message": "No permission"}, 403

        answer.delete_from_db()
        return {"code": 204, "message": "Delete Success!"}, 204


class QASearch(Resource):
    search_parser = parser.copy()
    search_parser.remove_argument("title")
    search_parser.remove_argument("content")

    @marshal_with(question_field, envelope="questions")
    def get(self):
        args = QASearch.search_parser.parse_args(strict=True)
        search_key = args["search_key"]

        questions = QuestionModel.query.filter(or_(QuestionModel.title.contains(search_key), QuestionModel.content.contains(search_key))).all()
        return questions
