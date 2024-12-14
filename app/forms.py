import re

from flask import flash
from flask_wtf import FlaskForm
from wtforms import (EmailField, PasswordField, SearchField, StringField,
                     SubmitField)
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=3, max=20)])

    display_name = StringField('Display Name', validators=[DataRequired(), Length(
        min=3, max=20)])

    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')


def validate_password(password):
    """
    Validates the password against custom requirements:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        flash("Password must be at least 8 characters long.", category='danger')
    if not re.search(r'[A-Z]', password):
        flash("Password must contain at least one uppercase letter.",
              category='danger')
    if not re.search(r'[a-z]', password):
        flash("Password must contain at least one lowercase letter.",
              category='danger')
    if not re.search(r'[0-9]', password):
        flash("Password must contain at least one number.", category='danger')
    if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        flash("Password must contain at least one special character.",
              category='danger')
    return None
