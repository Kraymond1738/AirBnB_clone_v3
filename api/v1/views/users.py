#!/usr/bin/python3
'''Blueprint for user API endpoints'''

from flask import jsonify, abort, request, make_response
from models import storage
from models.user import User
from api.v1.views import app_views


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_user_by_id(user_id=None):
    '''
    Get user(s) by ID or all users if ID is not provided

    Returns:
    - If ID provided and exists: User object as JSON
    - If ID provided and does not exist: 404 status code
    - If ID not provided: List of all users as JSON
    '''
    if user_id is None:
        users = storage.all(User)
        return jsonify([user.to_dict() for user in users.values()])

    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id=None):
    '''
    Delete user by ID

    Returns:
    - If user exists: Empty JSON object and 200 status code
    - If user does not exist: 404 status code
    '''
    if user_id is not None:
        user = storage.get(User, user_id)
        if user is not None:
            storage.delete(user)
            storage.save()
            return make_response(jsonify({}), 200)
    abort(404)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def post_user():
    '''
    Create new user

    Returns:
    - If JSON body provided and contains email and password keys:
    User object as JSON and 201 status code
    - If JSON body not provided or does not contain email or password keys:
    400 status code
    '''
    body = request.get_json()
    if body is None or type(body) is not dict:
        abort(400, description='Not a JSON')
    if 'email' not in body.keys():
        abort(400, description='Missing email')
    if 'password' not in body.keys():
        abort(400, description='Missing password')

    user = User(**body)
    user.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id=None):
    '''
    Update user by ID

    Returns:
    - If user exists and JSON body provided: Updated User object as JSON
    and 200 status code
    - If user does not exist: 404 status code
    - If JSON body not provided: 400 status code
    '''
    if user_id is None:
        abort(404)
    user = storage.get(User, user_id)
    if user is None:
        abort(404)

    body = request.get_json()
    if body is None:
        abort(400, description='Not a JSON')
    for key in body.keys():
        if key not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, key, body[key])
    user.save()
    return make_response(jsonify(user.to_dict()), 200)
