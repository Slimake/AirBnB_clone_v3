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
    """Handles api/v1/status route"""
    data = {'status': 'OK'}

    return jsonify(data)


@app_views.route('/stats')
def stats():
    """Handles api/v1/stats route"""
    data = {}

    for cls in classes.values():
        if cls.__name__ != 'BaseModel':
            data[cls.__tablename__] = storage.count(classes[cls.__name__])
    return jsonify(data)
