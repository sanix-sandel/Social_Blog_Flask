from app import db
from datetime import datetime

from werkzeug.security import generate_password_hash, check_password_hash

from flask_login import UserMixin
from app import login

from hashlib import md5

followers=db.Table('followers',

    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)


class User(UserMixin, db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(64), index=True, unique=True)
    email=db.Column(db.String(120), index=True, unique=True)
    password_hash=db.Column(db.String(128))
    posts=db.relationship('Post', backref='author', lazy='dynamic')
    about_me=db.Column(db.String(140))
    last_seen=db.Column(db.DateTime, default=datetime.utcnow)
    
    followed=db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id==id),
        secondaryjoin=(followers.c.followed_id==id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic'
    )

    def set_password(self, password):
        self.password_hash=generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)    

    def avatar(self, size):
        digest=md5(self.email.lower().encode('utf-8')).hexdigest()
        return f"https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}"   

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    def is_following(self, user):
        return self.followed.filter(
            followers.c.followed_id==user.id
        ).count()>0                     

    def followed_posts(self):
        followed= Post.query.join(
            followers, (followers.c.followed_id==Post.user_id)).filter(
                followers.c.follower_id==self.id)
        own=Post.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Post.timestamp.desc())    


    def to_json(self):
        json_user={
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'about':self.about_me,
            'last_seen':self.last_seen
            
        }    
        return json_user

    def json_with_posts(self):
        json_user={
            'id':self.id,
            'username':self.username,
            'email':self.email,
            'about':self.about_me,
            'last_seen':self.last_seen,
            'posts':[post.to_json_for_user() for post in self.posts]
            
        }    
        return json_user   


    def generate_auth_token(self, expiration):
        s=Serializer(current_app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id':self.id}).decode('utf-8') 

    @staticmethod
    def verify_auth_token(token):
        s=Serializer(current_app.config['SECRET_KEY'])
        try:
            data=s.loads(token)
        except:
            return None
        return User.query.get(data['id'])                     

    def __repr__(self):
        return f'User {self.username}'


class Post(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(140), nullable=False)
    body=db.Column(db.String(140), nullable=False)
    timestamp=db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id=db.Column(db.Integer, db.ForeignKey('user.id'))


    def to_json(self):
        json_post={
            'id':self.id,
            'title':self.title,
            'body':self.body,
            'timestamp':self.timestamp,
            'user_id':self.user_id
            
        }
        return json_post

    def to_json_for_user(self):
        json_post={
            'id':self.id,
            'title':self.title,
            'body':self.body,
            'timestamp':self.timestamp,
           
            
        }
        return json_post


    @staticmethod
    def from_json(json_post):
        title=json_post.get('title')
        body=json_post.get('body')
        if body is None or body=='':
            raise ValidationError('post does not have a body')
        return Post(title=title, body=body)


    def __repr__(self):
        return f'<Post {self.title}>'        


@login.user_loader        
def load_user(id):
    return User.query.get(int(id))