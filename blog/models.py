from email.policy import default
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from sqlalchemy.sql import func

db = SQLAlchemy() 
DB_NAME = "blog_db"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    create_at = db.Column(db.DateTime(timezone = True), default = func.now())
    is_staff = db.Column(db.Boolean(), default = False)
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    create_at =  db.Column(db.DateTime(timezone=True), default=func.now())
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False)
    
    user = db.relationship('User',backref=db.backref('posts', cascade='delete'))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'), nullable=False)
    
    category = db.relationship('Category', backref=db.backref('category', cascade='delete'))
    
class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150),unique=True)
    
    def __repr__(self):
        return f'<{self.__class__.__name__}(name={self.name})>'
def get_user_model():
    return User

def get_post_model():
    return Post

def get_category_model():
    return Category
