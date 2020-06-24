from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, SubmitField
from wtforms.validators import (DataRequired, Email, EqualTo, Length,
                                ValidationError)

from flaskapp.models import User


class RegisterForm(FlaskForm):
    name = StringField('Name', validators=[
                       DataRequired(), Length(min=1, max=50)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm Password', validators=[
                            DataRequired(), EqualTo('password', message='Passwords do not match')])
    submit = SubmitField('Sign Up')

    # Custom validators, in case someone tries to register with already existing credentials
    def validate_name(self, name):
        user = User.query.filter_by(name=name.data).first()
        if user:
            raise ValidationError(
                'That name is taken. Please choose another one')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError(
                'That username is taken. Please choose another one')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError(
                'That email is taken. Please choose another one')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
