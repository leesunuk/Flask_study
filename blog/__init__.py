from flask import Flask
from .views import views
from .auth import auth
from .models import DB_NAME, db, get_user_model, get_post_model, get_category_model
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from pprint import pprint

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="IFP"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'
    admin = Admin(app, name='blog',
                  template_mode='bootstrap3')
    
    admin.add_view(ModelView(get_user_model(), db.session))
    admin.add_view(ModelView(get_post_model(), db.session))
    admin.add_view(ModelView(get_category_model(), db.session))
    
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