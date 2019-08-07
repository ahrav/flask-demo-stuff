from flask import Flask, jsonify


app = Flask(__name__)


@app.route("/store", methods=["POST"])
def create_store():
    pass


@app.route("/store/<string:name>")
def get_store(name):
    pass


app.run(port=5000)
