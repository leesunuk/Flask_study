from flask import Flask
from .views import views
from .auth import auth
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from pprint import pprint

db = SQLAlchemy()
DB_NAME = "blog_db"

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="IFP"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlit:///{DB_NAME}'
    db.init_app(app)
    
    app.register_blueprint(views, url_prefix="/blog")
    app.register_blueprint(auth, url_prefix="/auth")
    return app

def create_database(app):
    if not path.exists("blog/"+DB_NAME):
        db.create_all(app=app)