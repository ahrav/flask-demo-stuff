from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema

store_schema = StoreSchema()
store_schema_list = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            return store_schema.dump(store), 200
        return {"message": "store not found"}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": "store already exists"}, 400

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": "an error occurred"}, 500

            return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()

        return {"message": "store deleted"}


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": store_schema_list.dump(StoreModel.find_all())}
