#!/usr/bin/python3

"""
This module provides the status and stats API endpoints.
"""

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


CLASSES = {"amenities": Amenity, "cities": City, "places": Place,
           "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """
    Returns a JSON string with the status of the web server
    """
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    """
    Retrieves the number of objects for each class
    """
    stats_dict = {}
    for cls_name, cls in CLASSES.items():
        count = storage.count(cls)
        stats_dict[cls_name] = count
    return jsonify(stats_dict)
