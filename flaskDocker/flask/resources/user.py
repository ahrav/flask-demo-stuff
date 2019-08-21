from flask_restful import Resource
from flask import request
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt,
)
import traceback
from models.user import UserModel
from schemas.user import UserSchema
from blacklist import BLACKLIST


user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user_json = request.get_json()
        user = user_schema.load(user_json)

        if UserModel.find_by_username(user.username):
            return {"message": "Username already exists"}, 400

        if UserModel.find_by_email(user.email):
            return {"message": "Email already in use"}, 400

        try:
            user.save_to_db()
            return {"message": "User successfully registered"}, 201
        except:
            traceback.print_exc()
            user.delete_from_db()
            return {
                "message": """Internal server error creating user.
                Please try again"""
            }
