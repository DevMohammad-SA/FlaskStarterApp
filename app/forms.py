import re

from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (EmailField, PasswordField, SearchField, SelectField,
                     StringField, SubmitField, TextAreaField)
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class SignUpForm(FlaskForm):
    username = StringField('Username', validators=[
        DataRequired(), Length(min=3, max=20)])
    display_name = StringField('Display Name', validators=[
        DataRequired(), Length(min=3, max=20)])
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password',
        validators=[DataRequired(), EqualTo('password', message='Passwords must match')])
    submit = SubmitField('Sign Up')

    def validate_password(self, field):
        """
        Validates the password against custom requirements:
        - Minimum 8 characters
        - At least one uppercase letter
        - At least one lowercase letter
        - At least one number
        - At least one special character
        """
        password = field.data

        # Create a list to collect error messages
        errors = []

        # Password length check
        if len(password) < 8:
            errors.append("Password must be at least 8 characters long.")

        # Uppercase letter check
        if not re.search(r'[A-Z]', password):
            errors.append(
                "Password must contain at least one uppercase letter.")

        # Lowercase letter check
        if not re.search(r'[a-z]', password):
            errors.append(
                "Password must contain at least one lowercase letter.")

        # Number check
        if not re.search(r'[0-9]', password):
            errors.append("Password must contain at least one number.")

        # Special character check
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            errors.append(
                "Password must contain at least one special character.")

        # Raise a validation error if any errors were found
        if errors:
            raise ValidationError(' '.join(errors))


class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=20)])
    display_name = StringField('Display Name', validators=[Length(max=20)])
    email = EmailField('Email', validators=[Email(), Length(max=50)])
    bio = TextAreaField('Bio', validators=[Length(max=50)])
    avatar = FileField('Avatar', validators=[
                       FileAllowed(['jpg', 'jpeg', 'png'])])
    submit = SubmitField('Save')


class ChangePasswordForm(FlaskForm):
    new_password = PasswordField('New Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('new_password', message='Passwords must match')]
    )

    submit = SubmitField('Change Password')


class ChangeRoleForm(FlaskForm):
    new_role = SelectField(
        'Role', choices=[('user', 'User'), ('admin', 'Admin')])
    submit = SubmitField('Change Role')


class SearchForm(FlaskForm):
    query = SearchField('Search', validators=[DataRequired()])
    submit = SubmitField('Search')
