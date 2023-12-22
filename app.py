"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import connect_db, User, Post, datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://mac@localhost:5432/blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secret'


db = connect_db(app)
db.create_all()


@app.route("/")
def root_redirect():
    return redirect("/users")


@app.route("/users")
def user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("user-list.html", users=users)


@app.route("/users/new")
def get_new_user_form():
    return render_template("add-user.html")


@app.route("/users/new", methods=['POST'])
def add_new_user():
    f_name = request.form["first-name"]
    l_name = request.form["last-name"]
    image_url = request.form["image-url"]

    new_user = User(first_name=f_name, last_name=l_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()
    return redirect("/users")


@app.route("/users/<int:user_id>")
def get_user_by_id(user_id):
    user = User.query.get_or_404(user_id)
    user_post = Post.query.filter_by(user_id=user_id).all()
    return render_template("user-detail.html", user=user, user_posts=user_post)


@app.route("/users/<int:user_id>", methods=["POST"])
def POST_get_user_by_id(user_id):
    f_name = request.form["first-name"]
    l_name = request.form["last-name"]
    image_url = request.form["image-url"]

    user = User.query.get_or_404(user_id)
    user.first_name = f_name
    user.last_name = l_name
    user.image_url = image_url
    db.session.add(user)
    db.session.commit()

    return render_template("user-detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")


@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("new-post.html", user=user)


@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def POST_new_post(user_id):
    post_title = request.form["post-title"]
    post_content = request.form["post-content"]
    usr_id = user_id
    new_post = Post(title=post_title, content=post_content, user_id=usr_id)

    db.session.add(new_post)
    db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("post-detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("edit-post.html", post=post)


@app.route("/posts/<int:post_id>/edit", methods=["POST"])
def POST_edit_post(post_id):
    edited_title = request.form["post-title"]
    edited_content = request.form["post-content"]
    post = Post.query.get_or_404(post_id)

    post.title = edited_title
    post.content = edited_content

    db.session.add(post)
    db.session.commit()
    return redirect(f"/posts/{post_id}")


@app.route("/posts/<int:post_id>/delete", )
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    back = post.usr.id
    post = Post.query.filter_by(id=post_id).delete()

    db.session.commit()
    return redirect(f"/users/{back}")
