#!/usr/bin/python3
"""A view for City objects."""
from api.v1.views import app_views
from flask import jsonify, abort, Response, request
from models import storage
from models.city import City
from models.state import State


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_state_cities(state_id):
    """Gets cities of a state."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    cities = [city.to_dict() for city in state.cities]
    return jsonify(cities)


@app_views.route('/cities/<city_id>', methods=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Gets a city by id."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_city(city_id):
    """Deletes a city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return jsonify({}), 200


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city object."""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    city = request.get_json(silent=True)
    if city is None:
        abort(400, "Not a JSON")
    if 'name' not in city:
        abort(400, 'Missing name')
    city['state_id'] = state_id
    city = City(**city)
    storage.new(city)
    storage.save()
    return jsonify(city.to_dict()), 201


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a city object."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    update = request.get_json(silent=True)
    if update is None:
        abort(400, 'Not a JSON')
    for key, value in update.items():
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(city, key, value)
    storage.save()
    return jsonify(city.to_dict()), 200
