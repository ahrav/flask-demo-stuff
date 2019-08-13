from flask import request
from flask_jwt_extended import fresh_jwt_required, jwt_required
from flask_restful import Resource
from marshmallow import ValidationError

from models.item import ItemModel
from schemas.item import ItemSchema

BLANK_ERROR = "'{}' cannot be left blank!"
ITEM_NOT_FOUND = "Item not found"
ITEM_DELETED = "Item deleted"
INSERT_ERROR = "An error occurred inserting the item."
ITEM_ALREADY_EXISTS = "An item with name '{}' already exists."


item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            return item_schema.dump(item), 200
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    @fresh_jwt_required
    def post(cls, name: str):
        if ItemModel.find_by_name(name):
            return ({"message": ITEM_ALREADY_EXISTS.format(name)}, 400)

        item_json = request.get_json()
        item_json["name"] = name

        item = item_schema.load(item_json)

        try:
            item.save_to_db()
        except:
            return {"message": INSERT_ERROR}, 500

        return item_schema.dump(item), 201

    @classmethod
    @jwt_required
    def delete(cls, name: str):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": ITEM_DELETED}
        return {"message": ITEM_NOT_FOUND}, 404

    @classmethod
    def put(cls, name: str):
        item_json = request.get_json()

        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        else:
            item_json["name"] = name

            item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemList(Resource):
    def get(self):
        return {"items": item_list_schema.dump(ItemModel.find_all())}, 200
