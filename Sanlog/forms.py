from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms.validators import DataRequired, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()],
                           render_kw={'placeholder': 'Your name'})
    password = PasswordField('Password',
                             validators=[DataRequired(), Length(8, 128)],
                             render_kw={'placeholder': 'Your password'})
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class UpdatePhotoForm(FlaskForm):
    photo = FileField('Update Image', validators=[
                      FileRequired(), FileAllowed(['jpg'])],
                      render_kw={'enctype': 'multipart/form-data'})
    submit = SubmitField()
