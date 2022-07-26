"""
Author: Mia Tran
Description: This program holds classes for forms.
"""
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, StringField
from wtforms.validators import InputRequired, EqualTo, Email, NoneOf


class PostForm(FlaskForm):
    """
    Form for blog posts.
    """
    title = StringField('Title', [InputRequired()])
    content = TextAreaField('Content', [InputRequired()])


class RegisterForm(FlaskForm):
    """
    Form for registration.
    """
    username = StringField('Username',
                           [InputRequired(),
                            NoneOf(values=["admin"],
                                   message='You cannot register with that username.')])
    email = StringField('Email', [InputRequired(), Email()])
    password = PasswordField('Password', [InputRequired()])
    confirm = PasswordField('Confirm Password', [InputRequired(),
                                                 EqualTo('password',
                                                         message='Passwords must match.')])


class LoginForm(FlaskForm):
    """
    Form for login.
    """
    email = StringField('Email', [InputRequired()])
    password = PasswordField('Password', [InputRequired()])
