#!/usr/bin/python3
"""A view for place objects."""
from api.v1.views import app_views
from flask import jsonify, abort, Response, request
from models import storage, storage_t
from models.place import Place
from models.city import City
from models.user import User
from models.state import State
from models.amenity import Amenity


@app_views.route('/cities/<city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """Gets a list of all places in a city."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    places = [place.to_dict() for place in city.places]
    return jsonify(places)


@app_views.route('/places/<place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """Gets a place by id."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """Deletes a place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    storage.delete(place)
    storage.save()
    return jsonify({}), 200


@app_views.route('/cities/<city_id>/places', methods=['POST'],
                 strict_slashes=False)
def create_place(city_id):
    """Creates a place."""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    if 'user_id' not in data:
        abort(400, 'Missing user_id')
    user_id = data.get('user_id')
    user = storage.get(User, user_id)
    if user is None:
        abort(404)
    if 'name' not in data:
        abort(400, 'Missing name')
    data['city_id'] = city_id
    place = Place(**data)
    storage.new(place)
    storage.save()
    return jsonify(place.to_dict()), 201


@app_views.route('/places/<place_id>', methods=['PUT'],
                 strict_slashes=False)
def update_place(place_id):
    """Updates a place."""
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')
    for key, value in data.items():
        if key not in ['id', 'user_id', 'city_id', 'created_at', 'updated_at']:
            setattr(place, key, value)
    storage.save()
    return jsonify(place.to_dict()), 200


@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    Retrieves all Place objects depending
    of the JSON in the body of the request
    """
    data = request.get_json(silent=True)
    if data is None:
        abort(400, 'Not a JSON')

    states = data.get('states', [])
    cities = data.get('cities', [])
    amenities_ids = data.get('amenities', [])

    if not data or not states and not cities and not amenities_ids:
        all_places = storage.all(Place).values()
        return jsonify([place.to_dict() for place in all_places])

    places = set()

    if states:
        for state_id in states:
            state = storage.get(State, state_id)
            if state is not None:
                for city in state.cities:
                    for place in city.places:
                        places.add(place)

    if cities:
        for city_id in cities:
            city = storage.get(City, city_id)
            if city is not None:
                for place in city.places:
                    places.add(place)

    if not states and not cities:
        places = storage.all(Place).values()

    if amenities_ids:
        amenities = [storage.get(Amenity, amenity_id).to_dict()
                     for amenity_id in amenities_ids]
        if storage_t == 'db':
            places = [place for place in places if all(
                amenity in place.amenities for amenity in amenities
            )]
        else:
            places = [place for place in places if all(
                amenity_id in place.amenity_ids for amenity_id in amenities_ids
            )]
    return jsonify([place.to_dict() for place in places])
