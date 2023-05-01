from flask import jsonify
from api.v1.views import app_views

@app_views.route('/status')
def status():
    """ create a route status"""
    return jsonify({"status": "OK"})
