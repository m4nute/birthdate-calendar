from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User, Birthdate
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint("auth", __name__)


def validate_signup(e, fn, p1, p2):
    user = User.query.filter_by(email=e).first()
    if user:
        flash("Email already exists.", category="error")
        return 1
    elif len(e) < 4:
        flash("Email must be greater than 3 characters.", category="error")
        return 1
    elif len(fn) < 2:
        flash("First name must be greater than 1 character.", category="error")
        return 2
    elif p1 != p2:
        flash("Passwords don't match.", category="error")
        return 3
    elif len(p1) < 5:
        flash("Password must be at least 7 characters.", category="error")
        return 3
    else:
        new_user = User(
            email=e,
            first_name=fn,
            password=generate_password_hash(p1, method="sha256"),
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user, remember=True)
        flash("Account created!", category="success")
        return 0


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Incorrect password, try again.", category="error")
                return render_template(
                    "login.html", user=current_user, email=email, password=""
                )
        else:
            flash("Email does not exist.", category="error")
            return render_template(
                "login.html", user=current_user, email="", password=password
            )
    return render_template("login.html", user=current_user)


@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("auth.login"))


@auth.route("/sign_up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        first_name = request.form.get("firstName")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")
        result = validate_signup(email, first_name, password1, password2)
        if result == 1:
            return render_template(
                "sign_up.html",
                user=current_user,
                email="",
                first_name=first_name,
                password=password1,
            )
        elif result == 2:
            return render_template(
                "sign_up.html",
                user=current_user,
                email=email,
                first_name="",
                password=password1,
            )
        elif result == 3:
            return render_template(
                "sign_up.html",
                user=current_user,
                email=email,
                first_name=first_name,
                password="",
            )
        elif result == 0:
            return redirect(url_for("views.home"))
    return render_template("sign_up.html", user=current_user)
