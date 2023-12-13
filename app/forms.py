from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, FloatField, IntegerField, HiddenField, validators
from wtforms.validators import DataRequired, Email, EqualTo, Length, Optional, NumberRange


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=35)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password'), Length(min=5, max=35)])
    submit = SubmitField('Sign Up')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email(), Length(min=5, max=35)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=35)])
    submit = SubmitField('Login')


class SearchForm(FlaskForm):
    title = StringField('Movie Title', validators=[DataRequired(), Length(min=1, max=50)])
    submit = SubmitField('Search')


class MovieRatingForm(FlaskForm):
    rating = FloatField('Rating', validators=[DataRequired(), NumberRange(min=1, max=10, message="Rating must be "
                                                                                                 "between 1 and 10")])
    votes = HiddenField('Votes', validators=[Optional()])
    submit = SubmitField('Submit')
