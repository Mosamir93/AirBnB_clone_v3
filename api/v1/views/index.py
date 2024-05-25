#!/usr/bin/python3
"""Index module."""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status', methods=['Get'])
def get_status():
    """Returns a json of the status"""
    return jsonify({"status": "OK"})
