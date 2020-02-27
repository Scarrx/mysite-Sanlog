
# from markdown import markdown
from sqlalchemy import func
import yaml
from Sanlog import db, md, Admin, Article, Category, Tag, CategoryArticle, TagArticle, Comment
import codecs
from flask import (Flask, Response, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)
from flask import Blueprint
import os
from urllib.parse import urlencode, urljoin
from Sanlog.settings import website
blog_bp = Blueprint('blog', __name__)


@blog_bp.context_processor
def inject():
    return website


@blog_bp.route('/')
@blog_bp.route('/<int:page>')
def index(page=1):
    perpage = 10
    paginate = Article.query.order_by(
        Article.Changetimestamp.desc()).paginate(page, perpage, False)
    articles = paginate.items
    for article in articles:
        article.category = eval(article.category)
        article.tag = eval(article.tag)

    pages = paginate.pages
    if page == 1:
        prev = None
    else:
        prev = url_for('.index', page=page-1)
    if page == pages:
        next = None
    else:
        next = url_for('.index', page=page+1)
    return render_template('index.html', articles=articles, pages=pages, prev=prev, next=next)


@blog_bp.route('/archives')
@blog_bp.route('/archives/<int:page>')
def archives(page=1):
    perpage = 10
    paginate = Article.query.order_by(
        Article.Changetimestamp.desc()).paginate(page, perpage, False)
    articles = paginate.items
    year = 10000
    for article in articles:
        if article.Changetimestamp.year < year:
            article.new = True
            year = article.Changetimestamp.year

    pages = paginate.pages
    if page == 1:
        prev = None
    else:
        prev = url_for('.archives', page=page-1)
    if page == pages:
        next = None
    else:
        next = url_for('.archives', page=page+1)
    return render_template('archives.html', posts=articles, pages=pages, prev=prev, next=next)


@blog_bp.route('/tags')
def tags():
    tc = db.session.query(TagArticle.tagid, func.count(
        TagArticle.articleid).label("c")).group_by(TagArticle.tagid).subquery()
    posts = db.session.query(Tag.name, Tag.id, tc.c.c).filter(
        Tag.id == tc.c.tagid).all()
    return render_template('tags.html', posts=posts)


@blog_bp.route('/tag/<string:name>')
@blog_bp.route('/tag/<string:name>/<int:page>')
def tag(name, page=1):
    q = Tag.query.filter(Tag.name == name).first()
    if q is None:
        return 0, 404
    else:
        id = q.id
    posts = TagArticle.query.filter(
        TagArticle.tagid == id).with_entities(TagArticle.articleid).all()
    posts = [i.articleid for i in posts]
    perpage = 10
    paginate = Article.query.filter(Article.id.in_(posts)).order_by(
        Article.Changetimestamp.desc()).paginate(page, perpage, False)
    pages = paginate.pages
    posts = paginate.items
    if page == 1:
        prev = None
    else:
        prev = url_for('.tag', name=name, page=page - 1)
    if page == pages:
        next = None
    else:
        next = url_for('.tag', name=name, page=page + 1)

    return render_template('tag.html',
                           posts=posts, prev=prev, next=next, pages=pages, title=name)


@blog_bp.route('/categories')
def categories():
    cc = db.session.query(CategoryArticle.categoryid, func.count(
        CategoryArticle.articleid).label("c")).group_by(CategoryArticle.categoryid).subquery()
    posts = db.session.query(Category.name, Category.id, cc.c.c).filter(
        Category.id == cc.c.categoryid).all()
    return render_template('categories.html', posts=posts)


@blog_bp.route('/category/<string:name>')
@blog_bp.route('/category/<string:name>/<int:page>')
def category(name, page=1):
    Category
    q = Category.query.filter(Category.name == name).first()
    if q is None:
        return 0, 404
    else:
        id = q.id
    posts = CategoryArticle.query.filter(
        CategoryArticle.categoryid == id).with_entities(CategoryArticle.articleid).all()
    posts = [i.articleid for i in posts]
    perpage = 10
    paginate = Article.query.filter(Article.id.in_(posts)).order_by(
        Article.Changetimestamp.desc()).paginate(page, perpage, False)
    pages = paginate.pages
    posts = paginate.items
    if page == 1:
        prev = None
    else:
        prev = url_for('.category', name=name, page=page - 1)
    if page == pages:
        next = None
    else:
        next = url_for('.category', name=name, page=page + 1)

    return render_template('category.html',
                           posts=posts, prev=prev, next=next, pages=pages, title=name)


@blog_bp.route('/about')
def about():
    return render_template('about.html', about="THIS IS ABOUT")


@blog_bp.route('/search')
def search():
    return render_template('search.html')


@blog_bp.route('/test/<path:path>/')
def test(path):
    # return render_template('test.html')
    path = path.replace('/', '\\')
    with open('Sanlog\\source\\0001\\test.md', "r", encoding="utf-8") as f:
        h = f.read()

    # return markdown(h)
    # print(markdown(h, output_format='html', extensions=[
    #   'markdown.extensions.fenced_code', 'markdown.extensions.codehilite']))
    # return render_template('test.html', mark=markdown(h, extensions=['markdown.extensions.fenced_code', 'markdown.extensions.codehilite']))
    return render_template('post.html',
                           mark=md.convert(h),
                           post={"title": "TITLE",
                                 "time": "2020/02/26",
                                 "words": 19543},
                           prev={"title": "PPRREE"},
                           next={"title": "NNEEXX"},
                           comment={"num": 3},
                           nicheng="Sanwa",
                           gallery=[{"url": "head.png"}, {"url": "head.jpg"}, {"url": "head.png"}, {"url": "head.png"}])


@blog_bp.route('/blog/<int:id>/')
def blog(id):
    post = Article.query.get(id)
    if not post:
        return "404", 404
    prev = Article.query.order_by(Article.Changetimestamp.desc()).filter(
        Article.Changetimestamp > post.Changetimestamp).first()
    next = Article.query.order_by(Article.Changetimestamp.desc()).filter(
        Article.Changetimestamp < post.Changetimestamp).first()

    path = "Sanlog\\source"

    id = str(id).zfill(4)
    name = post.title + str(post.version).zfill(2) + '.md'
    post.tags = post.tag and eval(post.tag)
    post.category = post.category and eval(post.category)
    galary = post.galary and eval(post.galary)
    post.words = len(post.body)
    return render_template('post.html',
                           mark=md.convert(post.body),
                           post=post,
                           prev=prev,
                           next=next,
                           galary=galary,
                           comment={"num": 3},
                           nicheng="Sanwa",
                           )


@blog_bp.route("/blog/<path:url>")
def image(url):
    path = "Sanlog\\source"
    try:
        with open(os.path.join(path, url), "rb") as f:
            fr = f.read()
    except:
        return "", 404
    return fr


def markpre(mark):
    flag = "<!-- more -->"
    pre = mark.split("<!-- more -->")
    mark = flag.join(pre[1:])
    pre = pre[0]
    yml = pre.split("---")[1]
    data = yaml.load(yml)
    print(data)
    print(type(data))
