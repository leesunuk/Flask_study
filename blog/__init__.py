from flask import Flask
from .views import views
from .auth import auth
from .models import DB_NAME, db, get_user_model
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

from pprint import pprint

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="IFP"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    
    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/auth")
    
    create_database(app)
    
    login_manager = LoginManager()
    login_manager.login_view = "auth.login"
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user_by_id(id):
        return get_user_model().query.get(int(id))
    
    return app


def create_database(app):
    if not path.exists("blog/"+DB_NAME):
        db.create_all(app=app)