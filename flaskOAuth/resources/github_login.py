from flask import g, request, url_for
from flask_restful import Resource
from flask_jwt_extended import create_access_token, create_refresh_token
from oa import github

from models.user import UserModel


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(url_for("github.authorize", _external=True))


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        res = github.authorized_response()

        if res is None or res.get("access_token") is None:
            error_response = {
                "error": request.args["error"],
                "error_description": request.args["error_description"],
            }
            return error_response

        g.access_token = res["access_token"]
        github_user = github.get("user")
        github_username = github_user.data["login"]

        user = UserModel.find_by_username(github_username)

        if not user:
            user = UserModel(username=github_username, password=None)
            user.save_to_db()

        access_token = create_access_token(identity=user.id, fresh=True)
        refresh_token = create_refresh_token(user.id)

        return (
            {"access_token": access_token, "refresh_token": refresh_token},
            200,
        )
