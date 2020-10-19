from flask import render_template, redirect, flash

from app import app

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
    form=LoginForm()

    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data} {form.remember_me.data}")
        return redirect('/index')

    return render_template(
        'login.html',
        title='Sign in',
        form=form

    )