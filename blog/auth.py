from flask import Blueprint, flash, render_template, redirect, request, url_for
from flask_login import current_user, login_required, login_user, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import redirect
from .forms import LoginForm, SignupForm
from .models import User, get_user_model

db = SQLAlchemy()
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == "POST" and form.validate_on_submit():
        password = form.password.data
        user=get_user_model().query.filter_by(email=form.email.data).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in!", category='success')
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Password is incorrect!", category='error')
        else:
            flash("Email does not exist...", category='error')
    return render_template("login.html", form=form, user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.home"))

@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    form = SignupForm()
    if request.method == "POST" and form.validate_on_submit():
        signup_user = get_user_model()(
            email = form.email.data,
            username = form.username.data,
            password = generate_password_hash(form.password1.data),
        )
        
        email_exists = get_user_model().query.filter_by(email=form.email.data).first()
        username_exists = get_user_model().query.filter_by(username=form.username.data).first()
        
        if email_exists:
            flash('Email is already in use...', category='error')
        elif username_exists:
            flash('Username is already in use...', category='error')
        
        else:
            db.session.add(signup_user)
            db.session.commit()
            flash("User create!!!")
            return redirect(url_for("views.home"))
    return render_template("signup.html", form=form, user=current_user)
        
        
    email = request.form.get('email')
    print(email)
    
    username=request.form.get('username')
    print(username)
    
    password1=request.form.get('password1')
    print(password1)
    
    password2=request.form.get('password2')
    print(password2)
    
    return render_template("signup.html")