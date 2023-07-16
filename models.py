from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

class User(db.Model):
    """Blogly user"""

    __tablename__ = "users"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    first_name = db.Column(db.String(50),
                     nullable=False)
    last_name = db.Column(db.String(50),
                     nullable=False)
    img = db.Column(db.String(), nullable=True)

class Post(db.Model):
    """Blogly post"""

    __tablename__ = "post"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    title = db.Column(db.String(50),
                     nullable=False)
    content = db.Column(db.String(500),
                     nullable=False)
    created_at = db.Column(db.String(), nullable=False, default=datetime.now().strftime('%a %b %d %Y, %I:%M %p'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete="CASCADE"), nullable=False)

    tags = db.relationship('Tag', secondary='post_tag', backref='posts')
    
class Tag(db.Model):
    """Blogly tag"""

    __tablename__ = "tag"

    id = db.Column(db.Integer,
                   primary_key=True,
                   autoincrement=True)
    name = db.Column(db.String(100),
                     nullable=False)

class Post_tag(db.Model):
    """Tags relating to posts"""

    __tablename__ = "post_tag"

    post_id = db.Column(db.Integer,
                   db.ForeignKey('post.id', ondelete="CASCADE"),
                   primary_key=True)
    tag_id = db.Column(db.Integer,
                   db.ForeignKey('tag.id', ondelete="CASCADE"),
                   primary_key=True)
