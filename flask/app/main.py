import os
from flask import Flask, request, jsonify, render_template
from routes import route_blueprint

def create_app():
    application = Flask(__name__)
    application.register_blueprint(route_blueprint)
    return application

application = create_app()

if __name__ == "__main__":
    application.run(host='0.0.0.0', port=80, debug=True)
