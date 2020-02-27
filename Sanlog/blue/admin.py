
# from markdown import markdown
from Sanlog import pages, md
import codecs
from flask import (Flask, Response, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)
from flask import Blueprint
import os
from urllib.parse import urlencode, urljoin
from Sanlog.settings import website
admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/')
def admin():
    return "THIS iS AdMin"
