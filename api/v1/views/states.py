#!/usr/bin/python3
'''Blueprint for managing states'''

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>',
                 methods=['GET'],
                 strict_slashes=False)
def get_states(state_id=None):
    '''Retrieve all states or a specific state by ID'''

    if state_id is None:
        result = []
        states = storage.all(State).values()
        for state in states:
            result.append(state.to_dict())
        return jsonify(result)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    '''Delete a state by ID'''

    if state_id is not None:
        state = storage.get(State, state_id)
        if state is not None:
            storage.delete(state)
            storage.save()
            return make_response(jsonify({}), 200)

    abort(404)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    '''Create a new state'''

    request_data = request.get_json()
    if request_data is None or not isinstance(request_data, dict):
        abort(400, description='Not a JSON')
    if 'name' not in request_data:
        abort(400, description='Missing name')
    state = State(**request_data)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id=None):
    '''Update a state by ID'''

    if state_id is None:
        abort(404)

    state = storage.get(State, state_id)
    if state is None:
        abort(404)

    request_data = request.get_json()
    if request_data is None or not isinstance(request_data, dict):
        abort(400, description='Not a JSON')

    for key, value in request_data.items():
        if key not in ('id', 'created_at', 'updated_at'):
            setattr(state, key, value)

    state.save()
    return make_response(jsonify(state.to_dict()), 200)
