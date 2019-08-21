from ma import ma

# from marshmallow import pre_dump
from models.user import UserModel


class UserSchema(ma.ModelSchema):
    class Meta:
        model = UserModel
        load_only = ("password",)
        dump_only = ("id",)
