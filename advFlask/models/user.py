from flask import request, url_for
from requests import Response, post
from typing import Dict, Union

from db import db

UserJSON = Dict[str, Union[int, str]]

MAILGUN_DOMAIN = "sandbox23f2c3abc7694493bd6e5f8b76a819b2.mailgun.org"
MAILGUN_API_KEY = "13dd4f28fde2a0c4476f22fbb0c604fe-898ca80e-3ba42076"
FROM_TITLE = "Stores REST API"
FROM_EMAIL = "postmaster@sandbox23f2c3abc7694493bd6e5f8b76a819b2.mailgun.org"


class UserModel(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    activated = db.Column(db.Boolean, default=False)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username: str) -> "UserModel":
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, _id: int) -> "UserModel":
        return cls.query.filter_by(id=_id).first()

    def send_confirmation_email(self) -> Response:
        link = request.url_root[:-1] + url_for("userconfirm", user_id=self.id)

        return post(
            f"https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages",
            auth=("api", MAILGUN_API_KEY),
            data={
                "from": f"{FROM_TITLE} <{FROM_EMAIL}>",
                "to": self.email,
                "subject": "Registration Confirmation",
                "text": f"Please click link to confirm registration {link}",
            },
        )

