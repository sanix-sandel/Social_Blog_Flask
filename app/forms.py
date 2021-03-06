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

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username=original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user=User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username')    


class PostForm(FlaskForm):
    title=StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    body=TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])      
    submit=SubmitField('Submit')      