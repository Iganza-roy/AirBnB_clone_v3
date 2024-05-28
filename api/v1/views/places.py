#!/usr/bin/python3
"""Creates a view for places"""

from models import storage
from models.place import Place
from models.city import City
from models.state import State
from models.amenity import Amenity
from models.user import User
from api.v1.views import app_views
from flask import jsonify, request, abort


@app_views.route('/cities/<cities_id>/places',
                 methods=['GET'], strict_slashes=False)
def all_places_obj():
    """Retrieves a list of all place objects"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    places = storage.all(Place).values()
    return jsonify([place.to_dict() for place in places])


@app_views.route('/places/<place_id>',
                 methods=['GET'], strict_slashes=False)
def place_obj_id(place_id: str):
    """Retrieves place object using ID"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'])
def delete_place(place_id: str):
    """Deletes place object"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places',
                 methods=['POST'], strict_slashes=False)
def new_place():
    """Creates a Place"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    if not request.get_json():
        abort(400, description="Not a JSON")
    if 'user_id' not in request.get_json():
        abort(400, description="Missing user_id")

    data = request.get_json()
    user = storage.get(User, data['user_id'])

    if not user:
        abort(404)
    if 'name' not in request.get_json():
        abort(400, description="Missing name")

    data["city_id"] = city_id
    created_place = Place(**data)
    created_place.save()
    return jsonify(created_place.to_dict()), 201


@app_views.route('/places/<place_id>',
                 methods=['PUT'], strict_slashes=False)
def update_place(place_id: str):
    """Updates a place"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if not request.get_json:
        abort(400, description="Not a JSON")
    data = request.get_json()

    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id' 'created_at', 'updated_at']:
            setattr(place, key, value)
    place.save()
    return jsonify(place.to_dict()), 200
