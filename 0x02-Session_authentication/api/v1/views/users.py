#!/usr/bin/env python3
""" Module of Users views
"""
from api.v1.views import app_views
from flask import abort, jsonify, request
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def view_all_users() -> str:
    """GET /api/v1/users
    Returns:
        list of all User objects JSON represented
    """
    all_users = [user.to_json() for user in User.all()]
    return jsonify(all_users)


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def view_one_user(user_id: str = None) -> str:
    """GET /api/v1/users/:id
    Path parameter:
        - User ID
    Returns:
        User object JSON represented
        404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    if user_id == "me":
        if request.current_user is None:
            abort(404)
        user = request.current_user
        return jsonify(user.to_json())
    user = User.get(user_id)
    if user is None:
        abort(404)
    return jsonify(user.to_json())


@app_views.route('/users/<user_id>', methods=['DELETE'], strict_slashes=False)
def delete_user(user_id: str = None) -> str:
    """DELETE /api/v1/users/:id
    Path parameter:
        - User ID
    Returns:
        empty JSON is the User has been correctly deleted
        404 if the User ID doesn't exist
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)
    user.remove()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user() -> str:
    """POST /api/v1/users/
    JSON body:
        - email
        - password
        - last_name (optional)
        - first_name (optional)
    Returns:
        User object JSON represented
        400 if can't create the new User
    """
    rj = request.get_json()
    if rj is None or 'email' not in rj or 'password' not in rj:
        return jsonify({'error': 'Wrong format'}), 400

    try:
        user = User(**rj)
        user.save()
        return jsonify(user.to_json()), 201
    except Exception as e:
        return jsonify({'error': 'Can\'t create User: {}'.format(e)}), 400


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str = None) -> str:
    """PUT /api/v1/users/:id
    Path parameter:
        - User ID
    JSON body:
        - last_name (optional)
        - first_name (optional)
    Returns:
        User object JSON represented
        404 if the User ID doesn't exist
        400 if can't update the User
    """
    if user_id is None:
        abort(404)
    user = User.get(user_id)
    if user is None:
        abort(404)

    rj = request.get_json()
    if rj is None:
        return jsonify({'error': 'Wrong format'}), 400

    try:
        for key, value in rj.items():
            setattr(user, key, value)
        user.save()
        return jsonify(user.to_json()), 200
    except Exception as e:
        return jsonify({'error': 'Can\'t update User: {}'.format(e)}), 400