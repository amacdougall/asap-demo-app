import os
import pprint
from flask import Flask, request, jsonify, render_template
from pymongo import MongoClient

application = Flask(__name__)

MONGODB_URI = os.environ.get("MONGODB_URI")

client = MongoClient(MONGODB_URI, connectTimeoutMS=30000)
db = client["member-api"]

# application.config["MONGO_URI"] = os.environ.get("MONGO_URI")

@application.route("/")
def index():
    member = db.members.find_one()
    print("retrieved member from database: ", member)
    return jsonify({
        "message": "Hello world!",
        "member": member["first_name"]
    })

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True)
