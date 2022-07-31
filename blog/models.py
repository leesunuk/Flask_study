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
def get_user_model():
    return User

