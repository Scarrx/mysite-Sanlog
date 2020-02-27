
from markdown import Markdown
from flask_mail import Mail
from flask_moment import Moment
from flask_migrate import Migrate
from flask_wtf import CSRFProtect
from mdx_math import MathExtension
from flask_ckeditor import CKEditor
from flask_login import LoginManager
from flask_flatpages import FlatPages
from flask_sqlalchemy import SQLAlchemy
from flask_debugtoolbar import DebugToolbarExtension

md = Markdown(
    output_format='html',
    extensions=[
        'markdown.extensions.codehilite',
        'markdown.extensions.fenced_code',
        'markdown.extensions.attr_list',
        'markdown.extensions.footnotes',
        'markdown.extensions.nl2br',
        'markdown.extensions.toc',
        MathExtension(enable_dollar_delimiter=True),
    ]
)


FLATPAGES_AUTO_RELOAD = True
FLATPAGES_EXTENSION = '.md'
moment = Moment()
db = SQLAlchemy()
migrate = Migrate()
pages = FlatPages()
csrf = CSRFProtect()
ckeditor = CKEditor()
login_manager = LoginManager()
toolbar = DebugToolbarExtension()
