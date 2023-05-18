#!/usr/bin/python3
'''index blueprint'''

from api.v1.views import app_views
from flask import jsonify
from models import storage

from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User

<<<<<<< HEAD

classes = {"amenities": Amenity, "cities": City,
=======
CLASSES = {"amenities": Amenity, "cities": City,
>>>>>>> 37f16594d286a9df603fd06c1a4e3a852461a235
           "places": Place, "reviews": Review, "states": State, "users": User}


@app_views.route('/status')
def status():
    '''returns json object with the app status'''
    return jsonify({"status": "OK"})


@app_views.route('/stats')
def stats():
    '''retrieves the number of each objects by type'''
    result = {}
    for clss in classes:
        counter = storage.count(classes[clss])
        result[clss] = counter
    return jsonify(result)
