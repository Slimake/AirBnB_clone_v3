from models.state import State
from models import storage
from api.v1.views import app_views
from flask import abort, jsonify, request


@app_views.route('/states', methods=['GET'])
@app_views.route('/states/<state_id>', methods=['GET'])
def get_states(state_id=None):
    """
    Retrieves the list of State objects if state_id is None,
    Retrieves a state when state_id is provided
    """
    states = storage.all(State)
    objs = {}
    for key, value in states.items():
        objs[key] = value.to_dict()
    if state_id is None:
        return jsonify(list(objs.values()))

    state = storage.get(State, state_id)
    if state is not None:
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
        storage.delete(state)
        storage.save()
        return {}, 200
    else:
        abort(404)


@app_views.route('/states/', methods=['POST'])
def create_state():
    """Create State object"""
    obj = request.get_json()
    if not obj:
        return "Not a JSON", 400
    if 'name' not in obj:
        return "Missing name", 400

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
        return "Not a JSON", 400

    state.name = obj.get('name', state.name)
    state.save()
    return jsonify(state.to_dict()), 200
