from dotenv import load_dotenv
from flask_jwt_extended import JWTManager
from flask_restful import Api
from marshmallow import ValidationError

from blacklist import BLACKLIST
from db import db
from flask import Flask, jsonify
from ma import ma

app = Flask(__name__)
load_dotenv(".env", verbose=True)
app.config.from_object("default_config")  # load default config
app.config.from_envvar(
    "APPLICATION_SETTINGS"
)  # override with config.py for PROD

api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


@app.errorhandler(ValidationError)
def handle_marshmallow_validation(err):
    return jsonify(err.messages), 400


jwt = JWTManager(app)


@jwt.token_in_blacklist_loader
def check_token_in_blacklist(decrypted_token):
    return decrypted_token["jti"] in BLACKLIST


if __name__ == "main":
    db.init_app(app)
    ma.init_app(app)
    app.run(host="0.0.0.0")
