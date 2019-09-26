from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from cqrs_app.extensions import arango, db, es, login_manager
from cqrs_app.models.relational.user import User
from cqrs_app.models.relational.post import Post
from cqrs_app.models.graph.user import get_friends_of_friends
from cqrs_app.models.document.post import get_more_like_this

BP = Blueprint("main", __name__, template_folder="templates")


@BP.route("/")
@login_required
def index():
    return render_template("main/index.jinja2")


@BP.route("/user/<username>")
@login_required
def user_index(username):
    user = User.query.filter_by(username=username).one()
    return render_template("main/user_index.jinja2", user=user)


@BP.route("/user/<username>/friends-of-friends")
@login_required
def user_friends_of_friends(username):
    user = User.query.filter_by(username=username).one()
    fof = get_friends_of_friends(arango.db, username)

    return render_template("main/user_fof.jinja2", user=user, fof=fof)


@BP.route("/user/<username>/follow", methods=('POST',))
def handle_follow(username):
    pass


@BP.route("/user/<username>/unfollow", methods=('POST',))
def handle_unfollow(username):
    pass


@BP.route("/write-post", methods=('POST',))
def handle_write_post():
    title = request.form['title']
    body = request.form['body']

    current_user.write_post(title, body)

    db.session.commit()

    return redirect(url_for('.index'))


@BP.route("/post/<post_id>/more-like-this")
def post_more_like_this(post_id):
    post = Post.query.get(post_id)
    hits = get_more_like_this(es, post)

    return render_template("main/post_more_like_this.jinja2", post=post, hits=hits)


@BP.route("/login")
def login():
    return render_template("main/login.jinja2")


@BP.route("/login", methods=("POST",))
def handle_login():
    username = request.form["username"]
    user = User.query.filter_by(username=username).one()
    login_user(user)

    return redirect(url_for(".index"))


@BP.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for(".index"))


@login_manager.user_loader
def load_user(username):
    return User.query.filter_by(username=username).one()
