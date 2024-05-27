#!/usr/bin/python3
"""Creates a view for cities"""

from models import storage
from models.city import City
from models.state import State
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('states/state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def all_cities(state_id):
    """Retrieves a list of all city objects"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def city_with_id(city_id: str):
    """Retrieves city object using ID"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'])
def delete_city(city_id: str):
    """Deletes city object"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities', methods=['POST'], strict_slashes=False)
def create_city():
    """Creates a City"""
    if not request.json:
        abort(400, description="Not a JSON")
    if 'name' not in request.json:
        abort(400, description="Missing name")

    data = request.get_json()
    created_city = City(**data)
    created_city.save()
    return jsonify(created_city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id: str):
    """Updates a city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    city.save()
    return jsonify(city.to_dict()), 200
