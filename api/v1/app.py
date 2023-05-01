#!/usr/bin/python3
#API

from flask import Flask
from models import stoage
from api.v1.views import app_views


app = Flask(__name__)
app.register_blueprint(app_views)

