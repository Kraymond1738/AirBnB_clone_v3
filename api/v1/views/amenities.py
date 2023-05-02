#!/usr/bin/python3
'''Blueprint for Place-Amenity relationship'''

from flask import jsonify, abort, request, make_response
from models import storage, storage_type
from models.place import Place
from models.user import User
from models.amenity import Amenity
from api.v1.views import app_views


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities_in_place(place_id=None):
    '''Get all amenities in a place'''
    if place_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)

    res = []
    if storage_type != 'db':
        amenities = storage.all(Amenity)
        for amenity in amenities.values():
            if amenity.id in place.amenity_ids:
                res.append(amenity)
    else:
        res = place.amenities

    return jsonify([amenity.to_dict() for amenity in res])


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity_from_place(place_id=None, amenity_id=None):
    '''Delete an amenity from a place'''
    if place_id is None or amenity_id is None:
        abort(404)
    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)
    if place is None or amenity is None:
        abort(404)

    if storage_type != 'db':
        if amenity.id not in place.amenity_ids:
            abort(404)
        index = None
        for idx, amenity_id in enumerate(place.amenity_ids):
            if amenity.id == amenity_id:
                index = idx
                break
        del place.amenity_ids[index]
        place.save()
    else:
        index = None
        for idx, amenity in enumerate(place.amenities):
            if amenity.id == amenity_id:
                index = idx
                break
        if index is None:
            abort(404)
        del place.amenities[index]
        place.save()

    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>', methods=['POST'],
                 strict_slashes=False)
def link_amenity_to_place(place_id=None, amenity_id=None):
    '''Link an amenity to a place'''
    if place_id is None or amenity_id is None:
        abort(404)

    place = storage.get(Place, place_id)
    amenity = storage.get(Amenity, amenity_id)

    if place is None or amenity is None:
        abort(404)

    if storage_type != 'db':
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenity_ids.append(amenity_id)
            place.save()
            return make_response(jsonify(amenity.to_dict()), 201)
    else:
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        else:
            place.amenities.append(amenity)
            place.save()
            return make_response(jsonify(amenity.to_dict()), 201)
