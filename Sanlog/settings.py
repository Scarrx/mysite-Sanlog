# -*- coding: utf-8 -*-
import os
import sys
import json
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

print(sys.platform)

# WIN = sys.platform.startswith('win')
# if WIN:
#     prefix = 'sqlite:///'
# else:
#     prefix = 'sqlite:////'


# DBMS:URI
# MySQL:mysql://username:password@host/databasename

prefix = "mysql://"


class BaseConfig:
    #
    SECRET_KEY = os.getenv('SECRET_KEY', 'Sanwa key')
    # dont know
    DEBUG_TB_INTERCEPT_REDIRECTS = False

    # 是否追踪对象的修改
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_RECODE_QUERIES = True

    SQL_USERNAME = os.getenv("SQL_USERNAME", "root")
    SQL_PASSWORD = os.getenv("SQL_PASSWORD", "PASSWORD")
    # CKEDITOR_ENABLE_CSRF = True
    # CKEDITOR_FILE_UPLOADER = 'admin.upload_image'

    # MAIL_SERVER = os.getenv('MAIL_SERVER')
    # MAIL_PORT = 465
    # MAIL_USE_SSL = True
    # MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    # MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    # MAIL_DEFAULT_SENDER = ('Bluelog Admin', MAIL_USERNAME)

    # BLUELOG_EMAIL = os.getenv('BLUELOG_EMAIL')
    # BLUELOG_POST_PER_PAGE = 10
    # BLUELOG_MANAGE_POST_PER_PAGE = 15
    # BLUELOG_COMMENT_PER_PAGE = 15

    # BLUELOG_THEMES = {'perfect_blue': 'Perfect Blue',
    #                   'black_swan': 'Black Swan'}
    # BLUELOG_SLOW_QUERY_THRESHOLD = 1

    # BLUELOG_UPLOAD_PATH = os.path.join(basedir, 'uploads')
    # BLUELOG_ALLOWED_IMAGE_EXTENSIONS = ['png', 'jpg', 'jpeg', 'gif']


class DevelopmentConfig(BaseConfig):
    SQLALCHEMY_DATABASE_URI = prefix+BaseConfig.SQL_USERNAME + \
        ':'+BaseConfig.SQL_PASSWORD+'@localhost/Sanlog'
    # SQLALCHEMY_DATABASE_URI = prefix + os.path.join(basedir, 'data-dev.db')


# class TestingConfig(BaseConfig):
#     TESTING = True
#     WTF_CSRF_ENABLED = False
#     SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # in-memory database


# class ProductionConfig(BaseConfig):
#     SQLALCHEMY_DATABASE_URI = os.getenv(
#         'DATABASE_URL', prefix + os.path.join(basedir, 'data.db'))


config = {
    'development': DevelopmentConfig,
    # 'testing': TestingConfig,
    # 'production': ProductionConfig
}

website = {}
try:
    with open("Sanlog/website.json", "r") as f:
        website = json.load(f)
except Exception as e:
    print(e)
    print("website read error")
print(website)
