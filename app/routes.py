from flask import (render_template, 
                    redirect, 
                    flash,
                    url_for, request)
from flask_login import (current_user, 
                        login_user, logout_user,
                        login_required)
from werkzeug.urls import url_parse


from app import app

from app.models import*

from .forms import*

from datetime import datetime

@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen=datetime.utcnow()
        db.session.commit()


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def home():
    form=PostForm()
    posts=current_user.followed_posts().all()
    if form.validate_on_submit():
        post=Post(title=form.title.data, body=form.body.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live')
        return redirect(url_for('home'))
    return render_template('index.html', 
        title='Home', form=form, posts=posts)


@app.route('/login', methods=['GET', 'POST'])
def loginuser():

    if current_user.is_authenticated:
        return redirect(url_for('home'))

    form=LoginForm()

    if form.validate_on_submit():
        user=User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('loginuser'))
        login_user(user, remember=form.remember_me.data)
        #flash(f"Login requested for user {form.username.data} {form.remember_me.data}")
        next_page=request.args.get('next')
        if not next_page or not next_page.startswith('/'):
            next_page=url_for('home')
        return redirect(next_page)

    return render_template(
        'login.html',
        title='Sign in',
        form=form

    )



@app.route('/logout')
def logoutuser():
    logout_user()
    return redirect(url_for('loginuser'))

@app.route('/register', methods=['GET', 'POST'])
def registeruser():
    if current_user.is_authenticated:
        return redirect(url_for('home'))    
    form=RegistrationForm()
    if form.validate_on_submit():
        user=User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user !')
        return redirect(url_for('loginuser'))
    return render_template('register.html', title='Register', form=form)        


@app.route('/user/<username>') 
@login_required
def userprofile(username):
    user=User.query.filter_by(username=username).first_or_404()
    posts=[
        {'author':user, 'body':'Test post #1'},
        {'author':user, 'body':'Test post #2'}
    ]  
    return render_template('user.html', user=user, posts=posts) 


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form=EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username=form.username.data
        current_user.about_me=form.about_me.data
        db.session.commit()
        flash('Your changes have been saved')
        return redirect(url_for('edit_profile'))
    elif request.method=='GET':
        form.username.data=current_user.username
        form.about_me.data=current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)        



@app.route('/follow/<username>')
@login_required
def follow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found. ')
        return redirect(url_for('home'))
    if user == current_user:
        flash('You cannot follow yourself !')
        return redirect(url_for('user', username=username))
    current_user.follow(user) 
    db.session.commit()
    flash(f'You are following {username}')
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user=User.query.filter_by(username=username).first()
    if user is None:
        flash(f'User {username} not found')
        return redirect(url_for('home'))
    if user == current_user:
        flash('You can unfollow yourself !')
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(f'You are not following {username}.')
    return redirect(url_for('user', username=username))                   



@app.route('/explore')
@login_required
def explore():
    posts=Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('index.html', title='Explore', posts=posts)    