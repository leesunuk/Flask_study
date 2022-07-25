from flask import Blueprint, render_template

views = Blueprint("views", __name__)

@views.route("/")
def home():
    return render_template("index.html")

@views.route("/about")
def about():
    return render_template("about.html")

@views.route("/categories-list")
def categories_list():
    return render_template("categories_list.html")

@views.route("/post-list")
def post_list():
    return render_template("post.html")

@views.route('posts/<int:id>')
def post_detail():
    return render_template("post_detail.html")

@views.route("/contact")
def contact():
    return render_template("contact.html")