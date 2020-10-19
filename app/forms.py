from flask_wtf import FlaskForm
from wtforms import*
from wtforms.validators import*
from  email_validator import*
from .models import User



class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('password1', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign in')


class RegistrationForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    email=StringField('Email', validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    password2=PasswordField('Repeat password', validators=[DataRequired(), EqualTo('password')])
    submit=SubmitField('Register')

    def validate_username(self, username):
        user=User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username')

    def validate_email(self, email):
        user=User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.') 


class EditProfileForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    about_me=StringField('about_me', validators=[Length(min=0, max=140)])
    submit=SubmitField('Submit')        