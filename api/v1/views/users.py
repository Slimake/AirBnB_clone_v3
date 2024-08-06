#!/usr/bin/python3
"""
users module

This module contains the views for handling User objects in the API.
It defines routes for retrieving, creating, updating,
and deleting User objects.
"""

from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/users', methods=['GET'])
def get_users():
    """
    Retrieves the list of all User objects
    """
    user_list = [
        user.to_dict()
        for user in storage.all(User).values()]
    return jsonify(user_list)


@app_views.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """
    Retrieves a User object using user_id
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """
    Deletes User object if user_id exist
    """
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    user.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'])
def create_user():
    """Create User object"""
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'email' not in obj_data:
        return jsonify({"error": "Missing email"}), 400
    if 'password' not in obj_data:
        return jsonify({"error": "Missing password"}), 400

    user = User(**obj_data)
    user.save()
    return jsonify(user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Update User object"""
    user_obj = storage.get(User, user_id)
    if user_obj is None:
        abort(404)
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400

    user_obj.password = obj_data['password']
    user_obj.save()
    return jsonify(user_obj.to_dict()), 200
