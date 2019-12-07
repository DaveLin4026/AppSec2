from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
#https://wtforms.readthedocs.io/en/stable/crash_course.html

from wtforms.validators import DataRequired


class BaseUserForm(FlaskForm):
    username = StringField("Username", id="uname", validators=[DataRequired()])
    password = PasswordField("Password", id="pword", validators=[DataRequired()])
    two_factor = StringField("2fa", id="2fa")


class LoginForm(BaseUserForm):
    submit = SubmitField("Login")


class RegisterForm(BaseUserForm):
    submit = SubmitField("Register")


class SpellCheckForm(FlaskForm):
    inputarea = StringField("input text", id="input text")
    submit = SubmitField("Click Here")


class UserSearchForm(FlaskForm):
    username = StringField("Username", id="userquery", validators=[DataRequired()])
    submit = SubmitField("Search")
