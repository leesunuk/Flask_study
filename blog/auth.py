from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from .forms import SignupForm
from .models import User

db = SQLAlchemy()
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return redirect("views.blog_home")

@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        signup_user = User(
            email = form.email.data,
            username = form.username.data,
            password = generate_password_hash(form.password1.data),
        )
        
        email_exists = User.query.filter_by(email=form.email.data).first()
        username_exists = User.query.filter_by(username=form.username.data).first()
        
        if email_exists:
            flash('Email is already in use...', category='error')
        elif username_exists:
            flash('Username is already in use...', category='error')
        
        else:
            db.session.add(signup_user)
            db.session.commit()
            flash("User create!!!")
            return redirect(url_for("views.home"))
    return render_template("signup.html", form=form)
        
        
    email = request.form.get('email')
    print(email)
    
    username=request.form.get('username')
    print(username)
    
    password1=request.form.get('password1')
    print(password1)
    
    password2=request.form.get('password2')
    print(password2)
    
    return render_template("signup.html")