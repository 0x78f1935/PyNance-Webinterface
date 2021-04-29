from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

class SystemApiView(FlaskView):
    
    decorators = [ ]

    def get(self):
        """Returns system details

        Returns:
            {
                "authentication": false, 
                "language": "en", 
                "token": "", 
                "version": "3.0.0"
            }
        """
        from backend.models.system import SystemModel
        system = SystemModel.query.first()
        return jsonify(system.to_dict(['id', 'updated', 'password'])), 200

    @route('/create', methods=['POST'])
    def create(self):
        from backend.models.system import SystemModel
        system = SystemModel.query.first()
        if request.headers['sk'] == current_app.config['SECRET_KEY']:
            system.set_password(request.json['pwd'])
            system.update_data({'authentication': True, 'tos': True})
        return jsonify(system.to_dict(['id', 'updated', 'password'])), 200

    @login_required
    def post(self):
        from backend.models.system import SystemModel
        system = SystemModel.query.first()
        if 'pwd' in request.json.keys():
            pwd = request.json['pwd']
            if system.check_password(pwd):
                return jsonify({current_app.config['SECRET_KEY']: True}), 200
        return jsonify({'succes': False}), 200
