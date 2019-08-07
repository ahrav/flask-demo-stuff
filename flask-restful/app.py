from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []


class Student(Resource):
    def get(self, name):
        item = [item for item in items if item["name"] == name]
        if item:
            return item
        return {"item": None}, 404

    def post(self, name):
        item = {"name": name, "price": 32.00}
        items.append(item)
        return item


api.add_resource(Student, "/student/<string:name>")

app.run()
