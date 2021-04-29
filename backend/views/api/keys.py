from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance


class KeysApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.keys import KeysModel
        model = KeysModel.query.all()
        return jsonify([i.to_dict() for i in model])
