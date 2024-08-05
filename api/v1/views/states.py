#!/usr/bin/python3
"""
states module

This module contains the views for handling State objects in the API.
It defines routes for retrieving, creating, updating,
and deleting State objects.
"""

from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'])
def get_states():
    """
    Retrieves the list of State objects
    """
    state_list = [state.to_dict() for state in storage.all(State).values()]
    return jsonify(state_list)


@app_views.route('/states/<state_id>', methods=['GET'])
def get_state_id(state_id):
    """
    Retrieves a state when state_id is provided
    """
    state = storage.get(State, state_id)
    if state:
        return jsonify(state.to_dict())
    else:
        abort(404)


@app_views.route('/states/<state_id>', methods=['DELETE'])
def delete_state(state_id):
    """
    Delete the State object if state_id exists
    """
    state = storage.get(State, state_id)
    if state:
        state.delete()
        storage.save()
        return jsonify({}), 200
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Create State object"""
    obj = request.get_json()
    if not obj:
        return jsonify({"error": "Not a JSON"}), 400
    if 'name' not in obj:
        return jsonify({"error": "Missing name"}), 400

    state = State(**obj)
    state.save()
    return jsonify(state.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'])
def update_state(state_id):
    """Create State object"""
    state = storage.get(State, state_id)
    obj = request.get_json()
    if not state:
        abort(404)
    if not obj:
        return jsonify({"error": "Not a JSON"}), 400

    state.name = obj['name']
    state.save()
    return jsonify(state.to_dict()), 200
