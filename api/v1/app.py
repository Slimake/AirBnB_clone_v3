#!/usr/bin/python3
"""
app module
"""
from flask import Flask, jsonify
from models import storage
from api.v1.views import app_views
import os

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontent(exception):
    """For performing cleanup when the application context is destroyed """
    storage.close()


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Not found"}), 404


if __name__ == '__main__':
    HBNB_API_HOST = os.getenv('HBNB_API_HOST', '0.0.0.0')
    HBNB_API_PORT = os.getenv('HBNB_API_PORT', 5000)
    app.run(host=HBNB_API_HOST, port=HBNB_API_PORT, threaded=True)
