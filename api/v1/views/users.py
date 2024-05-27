#!/usr/bin/python3
"""Creates a view for Users"""

from models import storage
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/users', methods=['GET'], strict_slashes=False)
def all_users():
    """Retrieves a list of all User objects"""
    users = storage.all(User).values()
    return jsonify([user.to_dict() for user in users])


@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def user_with_id(user_id: str):
    """Retrieves user object using ID"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id: str):
    """Deletes user object"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    storage.delete(user)
    storage.save()
    return jsonify({}), 200


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Creates a User"""
    if not request.json:
        abort(400, description="Not a JSON")

    info = request.get_json()

    if 'name' not in info:
        abort(400, description="Missing email")

    if 'password' not in info:
        abort(4000, description="Missing password")

    created_user = User(**info)
    created_user.save()
    return jsonify(created_user.to_dict()), 201


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id: str):
    """Updates a user"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, value)
    user.save()
    return jsonify(user.to_dict()), 200
