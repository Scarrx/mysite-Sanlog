
# from markdown import markdown
from .. import pages, md
import codecs
from flask import (Flask, Response, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)
from flask import Blueprint
import os
from urllib.parse import urlencode, urljoin
from Sanlog.settings import website
H_bp = Blueprint('H', __name__)


HATH = 'E:/H/'


@H_bp.route('/')
@H_bp.route('/<path:hh>')
def image(hh=""):
    print(hh)
    if hh == "index":
        hh = ""
    path = os.path.join(HATH, hh)
    page = request.args.get("page", 0)
    page = int(page)

    if page == 0:
        pre_page = None
    else:
        pre_page = url_for('.image', hh=hh)+'?' + \
            urlencode([('page', str(page-1))])
    next_page = url_for('.image', hh=hh)+'?'+urlencode([('page', str(page+1))])
    print(os.path.isdir(path))
    if os.path.isdir(path):
        dirs = []
        images = []
        for i in os.listdir(path):
            if i.endswith(".jpg"):
                images.append(url_for('.H', hh=os.path.join(hh, i)))
            else:
                dirs.append({"i": i, "hh": url_for(
                    '.image', hh=os.path.join(hh, i))})
        if page * 30 + 30 > max(len(dirs), len(images)):
            next_page = None
        return render_template('image.html', dirs=dirs[30*page:30+30*page], images=images[30*page:30+30*page], pre_page=pre_page, next_page=next_page)
    else:
        # return redirect(url_for('.H', hh=hh))
        return H(hh)


@H_bp.route('/<path:hh>')
def H(hh):
    print("HH", hh)
    mimetype = None
    if hh.endswith('.jpg'):
        mimetype = 'image/jpeg'
    elif hh.endswith('mp4'):
        mimetype = 'audio/mp4'
    elif hh.endswith('avi'):
        minetype = 'audio/avi'
        return ""
    if mimetype is not None:
        with open(os.path.join('E:/H/', hh), "rb") as f:
            jpg = f.read()
        return Response(jpg, mimetype=mimetype)
    if hh.endswith('.txt'):
        mimetype = 'text'
    elif hh.endswith('.html'):
        mimetype = 'text/html'
    else:
        return
    try:
        with open(os.path.join(HATH, hh), "r", encoding='utf-8') as f:
            jpg = f.read()
    except:
        with open(os.path.join(HATH, hh), "r", encoding='gbk') as f:
            jpg = f.read()

    return Response(jpg.replace("\n", "<br>").replace("　　", "<br>"), mimetype=mimetype)
