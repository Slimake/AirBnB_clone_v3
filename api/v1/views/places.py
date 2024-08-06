#!/usr/bin/python3
"""
places module

This module contains the views for handling Place objects in the API.
It defines routes for retrieving, creating, updating,
and deleting Place objects.
"""

from models.place import Place
from models.city import City
from models.user import User
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/cities/<city_id>/places', methods=['GET'])
def get_places(city_id):
    """
    Retrieves the list of all Place objects of a City
    """
    place_list = [
        place.to_dict()
        for place in storage.all(Place).values()
        if place.city_id == city_id]
    if place_list == []:
        abort(404)
    return jsonify(place_list)


@app_views.route('/places/<place_id>', methods=['GET'])
def get_place(place_id):
    """
    Retrieves a Place object using place_id
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id):
    """
    Deletes a Place object if place_id exist
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'])
def create_place(city_id):
    """Create Place object"""
    obj_data = request.get_json()
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'user_id' not in obj_data:
        return jsonify({"error": "Missing user_id"}), 400
    if 'name' not in obj_data:
        return jsonify({"error": "Missing name"}), 400

    user_obj = storage.get(User, obj_data['user_id'])
    if user_obj is None:
        abort(404)

    obj_data['city_id'] = city_id
    place = Place(**obj_data)
    place.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'])
def update_place(place_id):
    """Update Place object"""
    place_obj = storage.get(Place, place_id)
    if place_obj is None:
        abort(404)
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400

    place_obj.name = obj_data['name']
    place_obj.description = obj_data['description']
    place_obj.number_rooms = obj_data['number_rooms']
    place_obj.number_bathrooms = obj_data['number_bathrooms']
    place_obj.max_guest = obj_data['max_guest']
    place_obj.price_by_night = obj_data['price_by_night']
    place_obj.latitude = obj_data['latitude']
    place_obj.longitude = obj_data['longitude']
    place_obj.save()
    return jsonify(place_obj.to_dict()), 200
