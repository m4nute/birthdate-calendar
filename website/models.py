from dataclasses import dataclass
from datetime import datetime
import string
from itsdangerous import Serializer
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func
import json


@dataclass
class Birthdate(db.Model):

    id: int
    first_name: string
    surname: string
    birthdate: datetime
    user_id: int

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    surname = db.Column(db.String(50))
    birthdate = db.Column(db.DateTime())
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))


class User(db.Model, UserMixin):

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    first_name = db.Column(db.String(150))
    birthdates = db.relationship("Birthdate")
