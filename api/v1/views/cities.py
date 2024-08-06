#!/usr/bin/python3
"""
cities module

This module contains the views for handling City objects in the API.
It defines routes for retrieving, creating, updating,
and deleting City objects.
"""

from models.state import State
from models.city import City
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states/<state_id>/cities', methods=['GET'])
def get_cities(state_id):
    """
    Retrieves the list of all City objects of a State
    """
    city_list = [
        city.to_dict()
        for city in storage.all(City).values()
        if city.state_id == state_id]
    if city_list == []:
        abort(404)
    return jsonify(city_list)


@app_views.route('/cities/<city_id>', methods=['GET'])
def get_city(city_id):
    """
    Retrieves a City object using city_id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id):
    """
    Deletes a City object if city_id exist
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)

    city.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'])
def create_city(state_id):
    """Create City object"""
    obj_data = request.get_json()
    state_obj = storage.get(State, state_id)
    if state_obj is None:
        abort(404)
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in obj_data:
        return jsonify({"error": "Missing name"}), 400

    obj_data['state_id'] = state_id
    city = City(**obj_data)
    city.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'])
def update_city(city_id):
    """Update City object"""
    city_obj = storage.get(City, city_id)
    if city_obj is None:
        abort(404)
    obj_data = request.get_json()
    if not obj_data:
        return jsonify({"error": "Not a JSON"}), 400

    city_obj.name = obj_data['name']
    city_obj.save()
    return jsonify(city_obj.to_dict()), 200
