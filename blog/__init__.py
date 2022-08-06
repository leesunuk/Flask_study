import email, click
from sqlalchemy.exc import IntegrityError
from flask import Flask, abort
from .views import views
from .auth import auth
from .models import DB_NAME, db, get_user_model, get_post_model, get_category_model
from flask_sqlalchemy import Model, SQLAlchemy
from os import path
from flask_login import LoginManager, current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from pprint import pprint
from werkzeug.security import generate_password_hash, check_password_hash
from wtforms import PasswordField, StringField
from wtforms.validators import InputRequired
from flask.cli import with_appcontext

def create_app():
    app=Flask(__name__)
    app.config["SECRET_KEY"]="IFP"
    
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    app.config['FLASK_ADMIN_SWATCH'] = 'Darkly'
    admin = Admin(app, name='blog',
                  template_mode='bootstrap3')
    
    class MyUserView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)
            
        class CustomPasswordField(StringField):
            def populate_obj(self, obj, name):
                setattr(obj, name, generate_password_hash(self.data))
            
        form_extra_fields = {'password': CustomPasswordField('Password', validators=[InputRequired()])}
        form_excluded_columns = {'post', 'created_at'}
    
    class MyPostView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)
        
        form_excluded_columns = {'created_at', 'comments'}
        
    class MyCategoryView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)
        
        form_excluded_columns = {'category'}
    
    class MyCommentView(ModelView):
        def is_accessible(self):
            if current_user.is_authenticated and current_user.is_staff == True:
                return True
            else:
                return abort(403)
        
    admin.add_view(MyUserView(get_user_model(), db.session))
    admin.add_view(MyPostView(get_post_model(), db.session))
    admin.add_view(MyCategoryView(get_category_model(), db.session))
    # admin.add_view(MyCommentView(get_comment_model(), db.session))
    
    
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
    

    @click.command(name="create_superuser")
    @with_appcontext
    def create_superuser():
        username = input("Enter username : ")
        email = input("Enter email : ")
        password = input("Enter password : ")
        is_staff = True
    
        try:
            superuser = get_user_model()(
                username = username,
                email = email,
                password =generate_password_hash(password),
                is_staff = is_staff
            )
            db.session.add(superuser)
            db.session.commit()
        except IntegrityError:
            print('\033[31m' + "Error : username or email already exists.")
        print(f"User created! : {email}")
    
    app.cli.add_command(create_superuser)
    return app

def create_database(app):
    if not path.exists("blog/"+DB_NAME):
        db.create_all(app=app)