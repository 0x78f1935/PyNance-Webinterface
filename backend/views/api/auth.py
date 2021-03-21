from flask_classful import FlaskView, route
from flask import jsonify, request, current_app

from backend.utils.auth import login_required
from backend import db, pynance

class AuthAPIView(FlaskView):

    @route('/create', methods=['POST'])
    def create(self):
        from backend.models.preference import PreferenceModel
        preferences = PreferenceModel.query.first()
        if request.headers['sk'] == current_app.config['SECRET_KEY']:
            preferences.set_password(request.json['pwd'])
            preferences.update_data({'authentication': True})
        return jsonify({
            'token': preferences.token,
            'authentication': preferences.authentication
        }), 200
   
    @login_required
    def post(self):
        from backend.models.preference import PreferenceModel
        preferences = PreferenceModel.query.first()
        if 'pwd' in request.json.keys():
            pwd = request.json['pwd']
            if preferences.check_password(pwd):
                return jsonify({current_app.config['SECRET_KEY']: True}), 200
        return jsonify({'succes': False}), 200
