import os

# from Note import Note
import click
from flask import (Flask, Response, flash, get_flashed_messages, redirect,
                   render_template, request, url_for)
# from flask_sqlalchemy import SQLAlchemy

# from forms import LoginForm, UpdatePhotoForm
# from flask_debugtoolbar import DebugToolbarExtension


# app = Flask(__name__)

# print(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv(
#     'DATABASE_URL', 'sqlite:///'+os.path.join(app.root_path, 'data.db'))
# app.secret_key = "this is my secret"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# db = SQLAlchemy(app)
# toolbar = DebugToolbarExtension(app)


# @app.cli.command()
# def hh():
#     """just hh
#     """
#     click.echo("hh")


@app.before_first_request
def before_first_request1():

    print("before_first_request this")


@app.before_request
def befoer_request1():
    print("before_request this")


@app.after_request
def after_request1(e):

    print("after_request_this")
    return e


@app.route('/')
def hello_world():
    return 'Hello,World2'


@app.route('/post/')
def hahahha():
    return "???"


@app.route('/get/<path:hh>')
def get(hh):
    print(hh)
    return hh


user = {
    'username': 'ZXF',
    'bio': "http://scarrr.top"
}
movies = [
    {'name': "123", "year": "1230"},
    {'name': "234", "year": "2340"},
]
HATH = 'E:/H/'


@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies)


# static\template\watch.html

@app.route('/image')
@app.route('/image/')
@app.route('/image/<path:hh>')
def image(hh=""):
    print(hh)
    if hh == "index":
        hh = ""
    path = os.path.join(HATH, hh)

    if os.path.isdir(path):
        res = ""
        for i in os.listdir(path):
            if i[-4:] == '.jpg':
                res += '<img src="%s">\n<br><\n>' % url_for('H',
                                                            hh=os.path.join(hh, i))
            elif i.endswith("qwe"):
                pass
            else:
                a = url_for('image', hh=hh)
                if a[-1] == '/':
                    pass
                else:
                    a += '/'
                res += '<a href="%s">%s</a>\n<br>\n' % ((a+i), i)
        return res
    else:
        return redirect(url_for('H', hh=hh))


@app.route('/H/<path:hh>')
def H(hh):
    with open(os.path.join('E:/H/', hh), "rb") as f:

        jpg = f.read()
    if hh.endswith('.jpg'):
        mimetype = 'image/jpeg'
    elif hh.endswith('mp4'):
        mimetype = 'audio/mp4'
    elif hh.endswith('avi'):
        minetype = 'audio/avi'
        return ""
    return Response(jpg, mimetype=mimetype)


# @app.route('/flash')
# def just_flash():
#     flash(u'é—ªç”µ')
#     return redirect(url_for('watchlist'))


# @app.route('/form')
# def form():
#     return render_template('form.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     # return render_template('login.html')
#     # form = LoginForm()
#     if request.method == 'POST' and form.validate():
#         print(form.data)
#     else:
#         print(form.errors)
#     return render_template('login.html', form=form)


# @app.route('/index')
# def index():
#     pass


# app.config['MAX_CONTENT_LENGTH'] = 10*1024*1024
# @app.route('/updateImage', methods=['GET', 'POST'])
# def updateImage():
#     form = UpdatePhotoForm()
#     if form.validate_on_submit():
#         print("form.image:", form.image)
#     else:
#         print("error:", form.errors)

#     return render_template('updateImage.html', form=form)


# if __name__ == '__main__':
#     app.run(debug=True, host='0.0.0.0', port=8000)
