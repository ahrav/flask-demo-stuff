from flask import g
from flask_restful import Resource
from oa import github


class GithubLogin(Resource):
    @classmethod
    def get(cls):
        return github.authorize(
            callback="http://localhost:5000/login/github/authorized"
        )


class GithubAuthorize(Resource):
    @classmethod
    def get(cls):
        res = github.authorized_response()
        g.access_token = res["access_token"]
        github_user = github.get("user")
        github_username = github_user.data["login"]
        return github_username
