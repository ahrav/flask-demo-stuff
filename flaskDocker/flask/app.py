from flask import Flask
from flask_restful import Resource, Api


app = Flask(__name__)
api = Api(app)


class Student(Resource):
    def get(self, name):
        return {"student": name}


api.add_resource(Student, "/api/v1/student/<string:name>")


if __name__ == "main":
    app.run(host="0.0.0.0")
