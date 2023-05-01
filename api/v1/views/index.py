#!/usr/bin/python3
'''status'''

from flask import jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from models.city import City
from models.places import Place
from models.review import Review
from models.state import State
from models.user import User


clss = { "amenities": Amenity, "cities": City, "places": Place, 
"reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    """ create a route status"""
    return jsonify({"status": "OK"})

@app_views.route('/stats')
def stats():
    """Retrieves each object by type"""
    rtn = {}
    for i in clss:
        count = storage.count(clss[i])
        rtn[i] = count
    return jsonify(rtn)
