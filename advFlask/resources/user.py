from flask import request, make_response, render_template
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    get_raw_jwt,
    jwt_refresh_token_required,
    jwt_required,
)
from flask_restful import Resource
from werkzeug.security import safe_str_cmp

from blacklist import BLACKLIST
from models.user import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()


class UserRegister(Resource):
    @classmethod
    def post(cls):
        user = user_schema.load(request.get_json())

        if UserModel.find_by_username(user.username):
            return {"message": "A user with that username already exists"}, 400

        user.save_to_db()
        user.send_confirmation_email()

        return (
            {
                "message": "User created successfully. Please check email for confirmation link"
            },
            201,
        )


class User(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        return user_schema.dump(user), 200

    @classmethod
    def delete(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.delete_from_db()
        return {"message": "User deleted"}, 200


class UserLogin(Resource):
    @classmethod
    def post(cls):
        user_data = user_schema.load(request.get_json(), partial=("email",))

        user = UserModel.find_by_username(user_data.username)
        if user and safe_str_cmp(user.password, user_data.password):
            if user.activated:
                access_token = create_access_token(
                    identity=user.id, fresh=True
                )
                refresh_token = create_refresh_token(user.id)
                return (
                    {
                        "access_token": access_token,
                        "refresh_token": refresh_token,
                    },
                    200,
                )
            return (
                {
                    "message": f"You have not confirmed email, please check your email {user.username}"
                },
                400,
            )
        return {"message": "invalid credentials"}, 401


class UserLogout(Resource):
    @classmethod
    @jwt_required
    def post(cls):
        jti = get_raw_jwt()["jti"]
        BLACKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200


class UserConfirm(Resource):
    @classmethod
    def get(cls, user_id: int):
        user = UserModel.find_by_id(user_id)
        if not user:
            return {"message": "User not found"}, 404
        user.activated = True
        user.save_to_db()
        headers = {"Content-Type": "text/html"}
        return make_response(
            render_template("confirmation_page.html", email=user.username),
            200,
            headers,
        )


class RefreshToken(Resource):
    @classmethod
    @jwt_refresh_token_required
    def post(cls):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user, fresh=False)
        return {"access_token": new_token}, 200
