"""Blogly application."""

from flask import Flask, redirect, render_template, request, flash
from models import connect_db, User, Post, PostTag, Tag

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

# ----------------**USERS view functions**------------------


@app.route("/users")
def user_list():
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template("/user-files/user-list.html", users=users)


@app.route("/users/new")
def get_new_user_form():
    return render_template("/user-files/add-user.html")


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
    return render_template("/user-files/user-detail.html", user=user, user_posts=user_post)


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

    return render_template("/user-files/user-detail.html", user=user)


@app.route("/users/<int:user_id>/edit")
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("/user-files/edit-user.html", user=user)


@app.route("/users/<int:user_id>/delete")
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect("/users")


# ----------------**POSTING view functions**------------------

@app.route("/users/<int:user_id>/posts/new")
def new_post(user_id):
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()
    return render_template("/post-files/new-post.html", user=user, tags=tags)


@app.route("/users/<int:user_id>/posts/new", methods=['POST'])
def POST_new_post(user_id):
    post_title = request.form["post-title"]
    post_content = request.form["post-content"]
    post_tags = request.form.getlist("post-tags")

    usr_id = user_id
    new_post = Post(title=post_title, content=post_content, user_id=usr_id)

    db.session.add(new_post)
    db.session.commit()

    last_post = Post.query.all()[-1]
    for tag in post_tags:
        tag_obj = Tag.query.filter_by(name=tag).first()
        attach_tag = PostTag(post_id=last_post.id, tag_id=tag_obj.id)
        db.session.add(attach_tag)
        db.session.commit()
    return redirect(f"/users/{user_id}")


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    post = Post.query.get_or_404(post_id)
    # tags = [tag for tag in post.tags]

    return render_template("/post-files/post-detail.html", post=post)


@app.route("/posts/<int:post_id>/edit")
def edit_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template("/post-files/edit-post.html", post=post)


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


@app.route("/posts/<int:post_id>/delete")
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    back = post.usr.id
    post = Post.query.filter_by(id=post_id).delete()

    db.session.commit()
    return redirect(f"/users/{back}")


# ----------------**TAGGING view functions**------------------

@app.route("/tags")
def tag_list():
    tags = Tag.query.all()
    # post_list = [n for post.id in Tag.posts]
    # print(tags.posts[0])
    # length = len(tags[1].posts)
    return render_template("/tags-files/tags-list.html", tags=tags)


@app.route("/tags/new")
def create_tag():
    return render_template("/tags-files/add-tag.html")


@app.route("/tags/new", methods=['POST'])
def POST_create_tag():
    tag_name = request.form["tag-name"]
    new_tag = Tag(name=tag_name)
    db.session.add(new_tag)
    db.session.commit()
    # return render_template("/tags-files/add-tag.html")
    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def tag_info(tag_id):
    chosen_tag = Tag.query.get_or_404(tag_id)

    return render_template("/tags-files/show-tagged-posts.html",

                           chosen_tag=chosen_tag)


@app.route("/tags/<int:tag_id>/edit")
def tag_edit(tag_id):
    chosen_tag = Tag.query.get_or_404(tag_id)

    return render_template("/tags-files/edit-tag.html", chosen_tag=chosen_tag)


@app.route("/tags/<int:tag_id>/edit", methods=["POST"])
def POST_tag_edit(tag_id):
    tag_name = request.form["tag-name"]

    chosen_tag = Tag.query.get_or_404(tag_id)
    chosen_tag.name = tag_name
    db.session.add(chosen_tag)
    db.session.commit()

    return redirect(f"/tags/{tag_id}")


# could not get the delete to work. it used to work before making the PostTag class (many-to-many)

# @app.route("/tags/<int:tag_id>/delete")
# def tag_delete(tag_id):

#     tag = Tag.query.get_or_404(tag_id)

#     db.session.delete(tag)
#     db.session.commit()
#     return redirect("/tags")
