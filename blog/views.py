from flask import Blueprint, abort, redirect, render_template, request, url_for
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

@views.route("/post-list/<int:id>")
def post_list(id):
    current_category = get_category_model().query.filter_by(id=id).first()
    posts = get_post_model().query.filter_by(category_id=id)
    return render_template("post_list.html", user=current_user, post=posts, current_category=current_category)

@views.route("/create-post", methods=['GET', 'POST'])
@login_required
def post_create():
    if current_user.is_staff == True:
        if current_user.is_staff == True:
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
                return render_template("create-post.html", user=current_user, categories=categories, form=form)
    else:
        return abort(403)
    

@views.route('/edit-post/<int:id>', methods=["GET", "POST"])
@login_required
def edit_post(id):
    post = db.session.query(get_post_model()).filter_by(id=id).first()
    form = PostForm()
    categories = get_category_model().query.all()
    
    if current_user.is_staff == True and current_user.username == post.user.username:
        if request.method == "GET":
            return render_template("post_edit_form.html",user=current_user, post=post, categories=categories, form=form)
        elif request.method == "POST" and form.validate_on_submit():
            post.title = form.title.data
            post.content = form.content.data
            post.category_id = int(form.category.data)
            db.session.commit()
            return redirect(url_for("views.home"))
    else:
        abort(403)
        
@views.route('/posts/<int:id>')
def post_detail(id):
    post = get_post_model().query.filter_by(id=id).first()
    return render_template("post_detail.html", user=current_user, post=post)

@views.route("/contact")
def contact():
    return render_template("contact.html", user=current_user)