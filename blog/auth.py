from flask import Blueprint, render_template, redirect, request

auth = Blueprint("auth", __name__)

@auth.route("/login", methods=['GET', 'POST'])
def login():
    return render_template("login.html")

@auth.route("/logout")
def logout():
    return redirect("views.blog_home")

@auth.route("/sign-up", methods=['GET', 'POST'])
def signup():
    
    email = request.form.get('email')
    print(email)
    
    username=request.form.get('username')
    print(username)
    
    password1=request.form.get('password1')
    print(password1)
    
    password2=request.form.get('password2')
    print(password2)
    
    return render_template("signup.html")