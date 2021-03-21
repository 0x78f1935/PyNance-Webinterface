from flask_classful import FlaskView, route
from flask import jsonify, request
from backend.utils.auth import login_required

from backend import db, pynance

class PreferenceAPIView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.preference import PreferenceModel
        preferences = PreferenceModel.query.first()
        return jsonify(preferences.to_dict(['id', 'password'])), 200
    
    def post(self):
        from backend.models.preference import PreferenceModel
        preferences = PreferenceModel.query.first()
        preferences.update_data(request.json)
        return jsonify(preferences.to_dict(['id', 'password'])), 200
