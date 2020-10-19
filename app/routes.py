from flask import render_template, redirect, flash
from flask_login import current_user, login_user

from app import app

from app.models import*



from .forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user={'username':'Sanix'}
    posts=[
        {
            'author':{'username':'John'},
            'body':{'Beauftiful day in Vancouver'}
        },
        {
            'author':{'username':'Susan'},
            'body':{'The avengers movie was so cool'}
        }
    ]
    return render_template('index.html', 
        title='Home', 
        user=user, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('index'))

    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        #flash(f"Login requested for user {form.username.data} {form.remember_me.data}")
        return redirect(url_for('/index'))

    return render_template(
        'login.html',
        title='Sign in',
        form=form

    )