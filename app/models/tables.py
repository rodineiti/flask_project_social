from app import db
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    name = db.Column(db.String)
    email = db.Column(db.String, unique=True)
    image = db.Column(db.String)

    def __init__(self, username, password, name, email):
        self.username = username
        self.password = password
        self.name = name
        self.email = email
    
    def __rep__(self):
        return "<User %r>" % self.username

class Post(db.Model):
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    content = db.Column(db.Text)
    image = db.Column(db.String)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)
    comments = db.relationship('Comment', backref='posts',lazy='dynamic')

    def __init__(self, title, content, user_id, image):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.image = image
    
    def __rep__(self):
        return "<Post %r>" % self.id

class Follow(db.Model):
    __tablename__ = "follow"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    follower_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    user = db.relationship('User', foreign_keys=user_id)
    follow = db.relationship('User', foreign_keys=follower_id)

    def __init__(self, user_id, follower_id):
        self.user_id = user_id
        self.follower_id = follower_id

    def __rep__(self):
        return "<Follow %r>" % self.id

class Comment(db.Model):
    __tablename__ = "comments"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
    body = db.Column(db.Text)

    user = db.relationship('User', foreign_keys=user_id)
    post = db.relationship('Post', foreign_keys=post_id)

    def __init__(self, user_id, post_id, body):
        self.user_id = user_id
        self.post_id = post_id
        self.body = body

    def __rep__(self):
        return "<Comment %r>" % self.id