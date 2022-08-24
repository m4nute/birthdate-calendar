from flask import (
    Blueprint,
    jsonify,
    redirect,
    render_template,
    request,
    flash,
    jsonify,
    url_for,
)
from flask_login import login_required, current_user
from jinja2 import Undefined
from .models import Birthdate
from . import db
import json
import datetime
import time
from flask import session


views = Blueprint("views", __name__)


def create_date(fn, s, b, _id):
    new_date = Birthdate(
        first_name=fn, surname=s, birthdate=transform_date(b), user_id=_id
    )
    db.session.add(new_date)
    db.session.commit()


def up_date(row):
    # update date
    db_row = Birthdate.query.filter_by(id=row["id"]).one()
    row["birthdate"] = transform_date(row["birthdate"])
    db_row.first_name = row["first_name"]
    db_row.surname = row["surname"]
    db_row.birthdate = row["birthdate"]
    db.session.commit()


def transform_date(date):
    date_split = date.split("-")
    date = datetime.date(int(date_split[0]), int(date_split[1]), int(date_split[2]))
    return date


def delete_id(ids):
    for _id in ids:
        Birthdate.query.filter_by(id=_id).delete()
        db.session.commit()


def vali_date(fn, s, b):
    if len(fn) < 2:
        flash("First name must be greater than 2 characters", category="error")
        return 1
    elif len(s) < 2:
        flash("Surname must be greater than 2 characters", category="error")
        return 2
    elif len(b) < 10 or len(b) > 10:
        flash("Birthdate is not correct, respect date format", category="error")
        return 3
    else:
        return 0


@views.route("/add", methods=["GET", "POST"])
@login_required
def add_day():
    if request.method == "POST":
        first_name = request.form.get("first_name")
        surname = request.form.get("surname")
        birthdate = request.form.get("birthdate")
        result = vali_date(first_name, surname, birthdate)
        if result == 0:
            create_date(first_name, surname, birthdate, current_user.id)
            flash("Date added", category="success")
            return redirect(url_for("views.home"))
        elif result == 1:
            return render_template(
                "add_day.html",
                user=current_user,
                first_name="",
                surname=surname,
                birthdate=birthdate,
            )
        elif result == 2:
            return render_template(
                "add_day.html",
                user=current_user,
                first_name=first_name,
                surname="",
                birthdate=birthdate,
            )
        elif result == 3:
            return render_template(
                "add_day.html",
                user=current_user,
                first_name=first_name,
                surname=surname,
                birthdate="",
            )
    return render_template("add_day.html", user=current_user)


@views.route("/update-row", methods=["POST", "GET"])
def update_rows():
    if request.method == "POST":
        row = json.loads(request.data)
        up_date(row)
        return render_template("api.html", user=current_user)
    return render_template("api.html", user=current_user)


@views.route("/delete-rows", methods=["POST", "GET"])
def delete_rows():
    if request.method == "POST":
        ids = json.loads(request.data)
        delete_id(ids)
        return render_template("api.html", user=current_user)
    return render_template("api.html", user=current_user)


@views.route("/api/birthdates", methods=["GET", "POST"])
@login_required
def convert_json():
    return jsonify(Birthdate.query.all())


@views.route("/", methods=["GET", "POST"])
@login_required
def home():
    return render_template("api.html", user=current_user)
