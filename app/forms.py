from flask_wtf import FlaskForm
from wtforms import*
from wtforms.validators import*

class LoginForm(FlaskForm):
    username=StringField('Username', validators=[DataRequired()])
    password=PasswordField('password1', validators=[DataRequired()])
    remember_me=BooleanField('Remember Me')
    submit=SubmitField('Sign in')
    