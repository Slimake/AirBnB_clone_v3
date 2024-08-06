#!/usr/bin/python3
"""
amenities module

This module contains the views for handling Amenity objects in the API.
It defines routes for retrieving, creating, updating,
and deleting Amenity objects.
"""

from models.amenity import Amenity
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/amenities', methods=['GET'])
def get_amenities():
    """
    Retrieves the list of all Amenity objects
    """
    amenity_list = [
        amenity.to_dict()
        for amenity in storage.all(Amenity).values()]
    return jsonify(amenity_list)


@app_views.route('/amenities/<amenity_id>', methods=['GET'])
def get_amenity(amenity_id):
    """
    Retrieves a Amenity object using amenity_id
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=['DELETE'])
def delete_amenity(amenity_id):
    """
    Deletes Amenity object if amenity_id exist
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)

    amenity.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'])
def create_amenity():
    """Create Amenity object"""
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in obj_data:
        return jsonify({"error": "Missing name"}), 400

    amenity = Amenity(**obj_data)
    amenity.save()
    return jsonify(amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'])
def update_amenity(amenity_id):
    """Update Amenity object"""
    amenity_obj = storage.get(Amenity, amenity_id)
    if amenity_obj is None:
        abort(404)
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400

    amenity_obj.name = obj_data['name']
    amenity_obj.save()
    return jsonify(amenity_obj.to_dict()), 200
