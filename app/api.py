from flask import jsonify, request
from .models import *
from app import app
from flask_login import current_user


@app.route('/api/posts/')
def get_posts():
    posts=Post.query.all()
    return jsonify({'posts':[post.to_json() for post in posts]})


@app.route('/api/posts/<int:id>')   
def post_detail(id):
    post=Post.query.get_or_404(id)
    return jsonify({'post':post.to_json()})
   

@app.route('/api/posts/delete/<int:id>')
def post_delete(id):
    post=Post.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    response=jsonify({'message':'post deleted'})
    return response

@app.route('/api/posts/new_post', methods=['POST'])
def new_post():
    post=Post.from_json(request.json)
    user=User.query.first()
    post.author=user
    db.session.add(post)
    db.session.commit()
    return jsonify(post.to_json())

@app.route('/api/posts/<int:id>/update', methods=['PUT'])
def update_post(id):
    post=Post.query.get_or_404(id)
    post.body=Post.from_json(request.json).body
    db.session.commit()
    return jsonify({'message':'post updated'})    


