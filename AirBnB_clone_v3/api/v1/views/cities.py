#!/usr/bin/python3
"""Handles all RESTFUL API actions for City objects"""
from api.v1.views import app_views
from flask import abort, jsonify, request, make_response
from models import storage
from models.city import City
from models.state import State


@app_views.route(
        '/states/<state_id>/cities', methods=['GET'], strict_slashes=False)
def get_cities_by_state(state_id):
    """Retrieves the list of all City objects of a State"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    all_cities = storage.all('City').values()

    return jsonify([city.to_dict() for city in all_cities
                    if city.state_id == state_id])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """Deletes a City Object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route(
        '/states/<state_id>/cities', methods=['POST'], strict_slashes=False)
def create_city(state_id):
    """Creates a City Object"""
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    if 'name' not in data:
        abort(400, 'Missing name')

    data['state_id'] = state_id
    city = City(**data)
    city.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    data = request.get_json()

    if data is None:
        abort(400, 'Not a JSON')
    ignore = ['id', 'state_id', 'created_at', 'updated_at']

    for key, value in data.items():
        if key not in ignore:
            setattr(city, key, value)
    city.save()
    return make_response(jsonify(city.to_dict()), 200)
