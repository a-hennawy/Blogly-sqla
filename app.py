"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import connect_db, User

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

    return render_template("user-detail.html", user=user)


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
