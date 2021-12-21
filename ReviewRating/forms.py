from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from ReviewRating.models import User

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	submit = SubmitField('Login')

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')
    
    def checkEmail(self,field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email has been registered already')

    def checkUsername(self,field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username Taken')

class SearchForm(FlaskForm):
    searchbox = StringField('Search Box', validators=[DataRequired()])
    submit = SubmitField('Search')

class ReviewForm(FlaskForm):
    review = StringField('Review Box', validators=[DataRequired()])
    submit = SubmitField('Submit')