# -*- coding: utf-8 -*-

import logging
import os
from logging.handlers import RotatingFileHandler, SMTPHandler

import click
from flask import Flask, Response, render_template, request
from flask_login import current_user
from flask_sqlalchemy import get_debug_queries
from flask_wtf.csrf import CSRFError


from .extensions import db, md, pages
from .models import (Admin, Article, Category, CategoryArticle, Comment, Tag,
                     TagArticle)
from .settings import config, website
from .blue import H_bp, admin_bp, blog_bp

basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))


def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_CONFIG', 'development')

    app = Flask('Sanlog')
    app.config.from_object(config[config_name])

    register_errors(app)
    register_logging(app)
    register_commands(app)
    register_extensions(app)
    register_blueprints(app)
    register_shell_context(app)
    register_request_handlers(app)
    register_template_context(app)

    return app


def register_errors(app):
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('errors/400.html'), 400

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('errors/500.html'), 500

    @app.errorhandler(CSRFError)
    def handler_csrf_error(e):
        return render_template('errors/400.html', description=e.description)


def register_logging(app):
    class RequestFormatter(logging.Formatter):
        def format(self, recode):
            recode.url = request.url
            recode.romote_addr = request.remote_addr
            return super(RequestFormatter, self).format(recode)

    request_formatter = RequestFormatter(
        '[%(asctime)s] %(remote_addr)s requested %(url)s\n'
        '%(levelname)s in %(module)s: %(message)s'
    )
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler = RotatingFileHandler(os.path.join(basedir, 'logs/Sanlog.log'),
                                       maxBytes=100 * 1024 * 1024, backupCount=10)
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # mail_handler = SMTPHandler(
    #     mailhost
    # )


def register_commands(app):
    @app.cli.command()
    @click.option('--drop', is_flag=True, help='Create after drop.')
    def initdb(drop):
        """Initialize the database."""
        if drop:
            click.confirm(
                "This operation will delete the database,Continue?", abort=True)
            db.drop_all()
            click.echo('Drop tables')
        db.create_all()
        click.echo('Initializef database.')

    @app.cli.command()
    @click.option('--username', prompt=True, help='THe username used to login.')
    @click.option('--password', prompt=True, hide_input=True,
                  confirmation_prompt=True, help='The password used to Login.')
    def init(username, password):
        """Building Sanlog"""
        click.echo('Initializing the database...')
        db.create_all()

        admin = Admin.query.first()
        if admin is not None:
            click.echo('the administrator already exists, updating...')
            admin.ursename = username
            admin.set_password(password)
        else:
            click.echo('Creating the temporary administrator account')
            admin = Admin(
                username=username,
                blog_title="Sanwa",
            )
            admin.set_password(password)
            db.session.add(admin)

        category = Category.query.first()
        if category is None:
            pass

        db.session.commit()
        click.echo('Done.')

    @app.cli.command()
    @click.option('--category', default=5, help='Quantity of categories, default is 10.')
    @click.option('--tag', default=5, help='Quantity of posts, default is 50.')
    @click.option('--article', default=35, help='Quantity of comments, default is 500.')
    def forge(category, tag, article):
        """Generate fake data."""
        from .fakes import fake_admin, fake_Category, fake_Tag, fake_Article

        db.drop_all()
        db.create_all()

        click.echo('Generating the administrator...')
        fake_admin()

        click.echo('Generating %d categories...' % category)
        fake_Category(category)

        click.echo('Generating %d Tags...' % tag)
        fake_Tag(tag)

        click.echo('Generating %d articles...' % article)
        fake_Article(article)

        click.echo('Done.')


def register_blueprints(app):
    app.register_blueprint(blog_bp)
    app.register_blueprint(admin_bp, url_prefix="/admin")
    app.register_blueprint(H_bp, url_prefix='/H')


def register_extensions(app):
    pages.init_app(app)
    db.init_app(app)
    # login_manager.init_app(app)
    # csrf.init_app(app)
    # ckeditor.init_app(app)
    # moment.init_app(app)
    # toolbar.init_app(app)
    # migrate.init_app(app)


def register_shell_context(app):
    @app.shell_context_processor
    def make_shell_context():
        return dict(db=db,
                    Admin=Admin,
                    Article=Article,
                    Tag=Tag,
                    Category=Category,
                    CategoryArticle=CategoryArticle,
                    TagArticle=TagArticle,
                    Comment=Comment)


def register_request_handlers(app):
    @app.after_request
    def query_profiler(response):
        # for q in get_debug_queries():
        #     if q.duration >= app.config['BLUELOG_SLOW_QUERY_THRESHOLD']:
        #         app.logger.warning(
        #             'Slow query: Duration: %fs\n Context: %s\nQuery: %s\n '
        #             % (q.duration, q.context, q.statement)
        #         )
        return response


def register_template_context(app):
    @app.context_processor
    def make_template_context():
        return website


# if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=8000)
