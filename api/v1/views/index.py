#!/usr/bin/python3
"""
Index view
"""
from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.engine.file_storage import classes


@app_views.route('/status')
def status():
    data = {'status': 'OK'}

    return jsonify(data)


@app_views.route('/stats')
def stat():
    data = {}
    dict_class = {
        "amenities": classes['Amenity'], "Cities": classes['City'],
        "places": classes['Place'], "reviews": classes['Review'],
        "states": classes['State'], "users": classes['User']}

    for cls in dict_class:
        data[cls] = storage.count(dict_class[cls])
    return jsonify(data)
