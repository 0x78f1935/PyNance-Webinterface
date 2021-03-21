from flask_classful import FlaskView, route
from flask import jsonify, request
from backend.utils.auth import login_required

from backend import db, pynance

class SettingsAPIView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.settings import SettingsModel
        settings = SettingsModel.query.first()
        return jsonify(settings.to_dict(['id'])), 200
   
    def post(self):
        from backend.models.settings import SettingsModel
        settings = SettingsModel.query.first()
        settings.update_data(request.json)
        return jsonify(settings.to_dict(['id'])), 200
