import os

import flask

from flask import Flask, flash, redirect, render_template, request, url_for, abort
from flask_login import (
    current_user,
    LoginManager,
    login_required,
    logout_user,
    login_user,
    UserMixin,
)
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash

from forms import LoginForm, RegisterForm, SpellCheckForm, UserSearchForm
from utils import run_spell_checker

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "testing")
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

from models import User, SpellCheck, Roles, UserActivity, create_database_users

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

db.create_all()
create_database_users()


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id=user_id).first()


@app.route("/")
def home():
    return redirect(url_for("login"))


@app.route("/register", methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = User(form.username.data, form.password.data)

            # TODO: add additional verification checks
            if user.username == "admin":
                user.role = Roles.admin
            try:
                user.save()
            except UniqueConstraintError:
                return render_template(
                    "login.html",
                    title="Register",
                    form=form,
                    form_title="Register",
                    registration_failure=True,
                )

            return render_template(
                "login.html",
                title="Register",
                form=form,
                form_title="Register",
                registration_success=True,
            )

        else:
            return render_template(
                "login.html",
                title="Register",
                form=form,
                form_title="Register",
                registration_failure=True,
            )

    return render_template(
        "login.html", title="Register", form=form, form_title="Register"
    )


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()

    if flask.request.method == "POST":
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user is None:
                return render_template(
                    "login.html",
                    title="Login",
                    form=form,
                    form_title="Login",
                    login_failure=True,
                )

            if not check_password_hash(user.password, form.password.data):
                abort(403)

            user.create_session()
            user = user.save()
            login_user(user)
            user_activity = UserActivity(activity_name="login", user=user)
            user_activity.save()
            return redirect(url_for("spell_checker"))
        else:
            return render_template(
                "login.html",
                title="Login",
                form=form,
                form_title="Login",
                login_failure=True,
            )

    # default is a GET request
    return render_template(
        "login.html", title="Login", form=form, form_title="David's Spell Checker" 
    )


@app.route("/spell_checker", methods=["GET", "POST"])
@login_required
def spell_checker():
    spell_checker_form = SpellCheckForm()

    if flask.request.method == "POST":
        if spell_checker_form.validate_on_submit():
            input_data = spell_checker_form.inputarea.data
            out = run_spell_checker(input_data)

            spell_checker = SpellCheck(
                text_to_check=input_data, result=out, user=current_user
            )
            spell_checker.save()
            return redirect("spell_checker")

    if flask.request.method == "GET":
        spell_checker = SpellCheck.query.filter_by(user_id=current_user.id).first()
        input_data = getattr(spell_checker, "text_to_check", None)

        login_success = request.args.get("login_success")
        return render_template(
            "spell_checker.html",
            title="Spell Checker",
            form=spell_checker_form,
            input_data=input_data,
            login_success=True,
        )


@app.route("/query_history", methods=["GET", "POST"])
@app.route("/query_history/query<qid>")
@login_required
def query_history(qid=None):
    user_search_form = UserSearchForm()

    if flask.request.method == "GET":
        spell_checker_queries = SpellCheck.query.filter_by(user_id=current_user.id).all()
        count = len(spell_checker_queries)

        if qid is not None:
            query = SpellCheck.query.filter_by(id=qid).first()
            if not query.can_be_accessed_by(current_user):
                abort(403)
        else:
            query = None

        return render_template(
            "spell_checker_history.html",
            queries=spell_checker_queries,
            count=count,
            qid=qid,
            searched_user=current_user,
            user=current_user,
            query=query,
            form=user_search_form,
        )

    if flask.request.method == "POST":
        if not current_user.role == Roles.admin:
            abort(403)

        if user_search_form.validate_on_submit():
            searched_user = User.query.filter_by(
                username=user_search_form.username.data
            ).first()

            searched_user_history = SpellCheck.query.filter_by(user_id=searched_user.id)

            return render_template(
                "spell_checker_history.html",
                queries=searched_user_history,
                count=len(searched_user_history.all()),
                searched_user=searched_user,
                qid=qid,
                user=current_user,
                query=searched_user_history,
                form=user_search_form,
            )


@app.route("/login_history", methods=["GET", "POST"])
@login_required
def login_history():
    user_search_form = UserSearchForm()

    if not current_user.role == Roles.admin:
        abort(403)

    if flask.request.method == "GET":
        return render_template(
            "login_history.html",
            searched_user=current_user,
            user=current_user,
            form=user_search_form,
        )

    if flask.request.method == "POST":
        if user_search_form.validate_on_submit():
            searched_user = User.query.filter_by(
                username=user_search_form.username.data
            ).first()
            searched_user_history = UserActivity.query.filter_by(
                user_id=searched_user.id
            ).all()
        return render_template(
            "login_history.html",
            searched_user=current_user,
            user=current_user,
            queries=searched_user_history,
            form=user_search_form,
        )


@app.route("/logout")
@login_required
def logout():
    user_id = current_user.id
    logout_user()
    user_activity = UserActivity(activity_name="logout", user_id=user_id)
    user_activity.save()
    return redirect(url_for("login"))
