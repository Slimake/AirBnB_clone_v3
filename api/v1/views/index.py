#!/usr/bin/python3
"""
Index view
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status')
def status():
    data = {'status': 'OK'}

    return jsonify(data)
