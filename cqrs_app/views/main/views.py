from flask import Blueprint, jsonify, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from cqrs_app.extensions import arango, db, login_manager
from cqrs_app.models.relational.user import User

BP = Blueprint("main", __name__, template_folder="templates")


@BP.route("/")
@login_required
def index():
    return render_template("main/index.jinja2")


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
