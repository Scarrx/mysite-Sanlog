# -*- coding: utf-8 -*-

from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from Sanlog import db
from sqlalchemy.schema import CreateTable


class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    blog_title = db.Column(db.String(60))
    # name
    # about

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)


class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    author = db.Column(db.String(30))
    title = db.Column(db.String(255), unique=True)

    typo = db.Column(db.Text, default="")
    body = db.Column(db.Text, default="")

    Createtimestamp = db.Column(
        db.DateTime, default=datetime.utcnow, index=True)
    Changetimestamp = db.Column(
        db.DateTime, default=datetime.utcnow, index=True)

    banner = db.Column(db.Text, default="")
    galary = db.Column(db.Text, default="")

    category = db.Column(db.Text)
    tag = db.Column(db.Text)

    version = db.Column(db.Integer)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True, index=True)
    name = db.Column(db.String(30), unique=True)


class Tag(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)


class CategoryArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    categoryid = db.Column(db.Integer, index=True)
    articleid = db.Column(db.Integer, index=True)


class TagArticle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tagid = db.Column(db.Integer, index=True)
    articleid = db.Column(db.Integer, index=True)


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    author = db.Column(db.String(30))
    email = db.Column(db.String(254))
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    avator = db.Column(db.Text, default="")
