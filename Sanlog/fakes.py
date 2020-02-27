# -*- coding: utf-8 -*-

from . import (Admin, Article, Category, CategoryArticle, Comment, Tag,
               TagArticle)
from . import db
from sqlalchemy.exc import IntegrityError
import random
import datetime

from faker import Faker
import os
fake = Faker()


def fake_admin():
    admin = Admin(
        username="admin",
        blog_title="Sanlog"
    )
    admin.set_password("password")
    db.session.add(admin)
    db.session.commit()


def fake_Category(count=5):
    for i in range(count):
        category = Category(
            name=fake.word()
        )
        db.session.add(category)
        try:
            db.session.commit()
        except:
            db.session.rollback()


def fake_Tag(count=5):
    for i in range(count):
        tag = Tag(
            name=fake.word()
        )
        db.session.add(tag)
        try:
            db.session.commit()
        except:
            db.session.rollback()


def fake_Article(count=35):
    for i in range(count):
        article = Article(
            author=fake.word(),
            title=fake.sentence(),
        )

        pre = fake.text(500)
        pro = fake.text(2000)
        body = pre + '\n<!-- more -->\n' + pro

        article.typo = pre

        cn = Category.query.count()
        ci = random.randint(1, cn+1)
        cl = []
        cli = []
        for j in range(ci):
            try:
                category = Category.query.get(random.randint(1, cn))
                if category.name not in cl:
                    cl.append(category.name)
                    cli.append(category.id)
            except:
                pass
        tn = Tag.query.count()
        ti = random.randint(1, tn+1)
        tl = []
        tli = []
        for j in range(ti):
            try:
                tag = Category.query.get(random.randint(1, tn))
                if tag.name not in tl:
                    tl.append(tag.name)
                    tli.append(tag.id)
            except:
                pass
        article.category = str(cl)
        article.tag = str(tl)
        article.version = random.randint(1, 5)
        time = datetime.datetime.utcnow()
        article.body = body
        body = '---\n' + 'title: ' + article.title + '\n' + 'date: ' + \
            str(time) + '\n' + 'categories: ' + \
            str(cl) + '\n' + 'tags :' + str(tl) + '\n---\n' + body
        article.Createtimestamp = time
        article.Changetimestamp = time
        db.session.add(article)
        db.session.commit()
        for c in cli:
            db.session.add(CategoryArticle(
                categoryid=c, articleid=article.id))
        for t in tli:
            db.session.add(TagArticle(tagid=t, articleid=article.id))
        dir = os.path.join('Sanlog\\source', str(article.id).zfill(4))
        try:
            if not os.path.exists(dir):
                os.makedirs(dir)
        except Exception as e:
            print(e)
            print("Fail", dir)
            pass
        with open(os.path.join(dir, article.title + str(article.version).zfill(2)+'.md'), "a+") as f:
            f.write(article.body)
        db.session.commit()
