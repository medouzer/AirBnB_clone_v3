#!/usr/bin/python3
"""City"""

from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from models.city import City


@app_views.route('states/<state_id>/cities',
                 methods=['GET'], strict_slashes=False)
def get_cities(state_id):
    """get cities of a state"""
    dict_cities = []
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    for city in state.cities:
        dict_cities.append(city.to_dict())
    return jsonify(dict_cities)


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """get city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    dict_city = city.to_dict()
    return jsonify(dict_city)


@app_views.route('/cities/<city_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_city(city_id):
    """delete city by id"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    storage.delete(city)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities',
                 methods=['POST'], strict_slashes=False)
def post_city(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    if req_data.get("name") is None:
        abort(400, 'Missing name')
    city = City(**req_data)
    city.state_id = state_id
    storage.save()
    dict_city = city.to_dict()
    return make_response(jsonify(dict_city), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'], strict_slashes=False)
def put_city(city_id):
    """updtae city"""
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    req_data = request.get_json(silent=True)
    if req_data is None:
        abort(400, 'Not a JSON')
    for key, value in req_data.items():
        if key not in ["id", "state_id", "created_at", "updated_at"]:
            setattr(req_data, key, value)
    req_data.save()
    state_dict = req_data.to_dict()
    return make_response(jsonify(state_dict), 200)
