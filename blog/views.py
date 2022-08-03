from flask import Blueprint, redirect, render_template, request, url_for
from flask_login import current_user, login_required
from flask_sqlalchemy import SQLAlchemy
from blog.forms import PostForm

from blog.models import get_category_model, get_post_model

db = SQLAlchemy()
views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
def home():
    return render_template("index.html", user=current_user)

@views.route("/about")
def about():
    return render_template("about.html", user=current_user)

@views.route("/categories-list")
def categories_list():
    categories = get_category_model().query.all()
    return render_template("categories_list.html", user=current_user, categories=categories)

@views.route("/post-list")
def post_list():
    return render_template("post.html", user=current_user)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def post_create():
    form = PostForm()
    if request.method == "POST" and form.validate_on_submit():
        post = get_post_model()(
            title=form.title.data,
            content=form.content.data,
            category_id=form.category.data,
            author_id=current_user.id,
        )
        db.session.add(post)
        db.session.commit()
        return redirect(url_for("views.home"))
    else:
        categories = get_category_model().query.all()
        return render_template("create-post.html", user=current_user, categories=categories)

@views.route('/posts/<int:id>')
def post_detail():
    return render_template("post_detail.html", user=current_user)

@views.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)