import os

from flask import Flask, jsonify, request
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy


# Init app
app = Flask(__name__)


if __name__ == "main":
    app.run(debug=True)
