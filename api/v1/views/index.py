#!/usr/bin/python3
"""index """

from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route("/status", methods=['GET'])
def statusof():
    """return the states ok"""
    return jsonify({"status": "OK"})


@app_views.route("/stats")
def stats():
    """retrieves the number of each objects by type"""
    all_counts = {
        "amenities": storage.count("amenities"),
        "cities": storage.count("cities"),
        "places": storage.count("places"),
        "reviews": storage.count("reviews"),
        "states": storage.count("states"),
        "users": storage.count("users")
    }
    return jsonify(all_counts)
