#!/usr/bin/python3
from models.state import State
from flask import jsonify, request, abort, make_response
from api.v1.views import app_views
from models import storage


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def gets_all_states():
    all_states = storage.all(State) .values()
    dict_states = [state.to_dict() for state in all_states]
    return jsonify(dict_states)


@app_views.route("/states/<state_id>", methods=["GET"], strict_slashes=False)
def states(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route("/states/<state_id>", methods=["DELETE"],
                 strict_slashes=False)
def states_delete(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    storage.delete(state)
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post():
    ask = request.get_json(silent=True)
    if ask is None:
        abort(400, 'Not a JSON')
    if ask.get("name") is None:
        abort(400, 'Missing name')
    state = State(**ask)
    state.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id):
    state = storage.get(State, state_id)
    if state is None:
        abort(404)
    state_data = request.get_json(silent=True)
    if state_data is None:
        abort(400, 'Not a JSON')
    excluded_keys = ['id', 'created_at', 'updated_at']
    for key, val in state_data.items():
        if key not in excluded_keys:
            setattr(state, key, val)
    state.save()
    return make_response(jsonify(state.to_dict()), 200)
# #!
# """states"""

# from api.v1.views import app_views
# from flask import jsonify, abort, request
# from models import storage
# from models.state import State


# @app_views.route('/states', methods=['GET'], strict_slashes=False)
# def get_states():
#     """get all states"""
#     states = storage.all(State).values()
#     for state in states:
#         dict_states = state.to_dict()
#     return jsonify(dict_states)


# @app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
# def get_stateid(state_id):
#     """get state by id"""
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     dict_state = state.to_dict()
#     return jsonify(dict_state)


# @app_views.route("/states/<state_id>",
#                  methods=["DELETE"], strict_slashes=False)
# def delete(state_id):
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     storage.delete(state)
#     storage.save()
#     return jsonify({}), 200


# @app_views.route('/states', methods=['POST'], strict_slashes=False)
# def post():
#     """post method"""
#     req_data = request.get_json()
#     if req_data is None:
#         abort(400, 'Not a JSON')
#     if "name" not in req_data:
#         abort(400, 'Missing name')
#     state = State(**req_data)
#     state.save()
#     state_dict = state.to_dict()
#     return jsonify(state_dict), 201


# @app_views.route('/states/<state_id>',
#                  methods=['PUT'], strict_slashes=False)
# def put(state_id):
#     state = storage.get(State, state_id)
#     if state is None:
#         abort(404)
#     req_data = request.get_json()
#     if req_data is None:
#         abort(400, 'Not a JSON')
#     for key, value in req_data.items():
#         if key not in ["id", "created_at", "updated_at"]:
#             setattr(state, key, value)
#     state.save()
#     state_dict = state.to_dict()
#     return jsonify(state_dict), 200
