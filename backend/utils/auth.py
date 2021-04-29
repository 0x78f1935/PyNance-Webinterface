from functools import wraps
from flask import request, jsonify, current_app


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        from backend.models.system import SystemModel
        system = SystemModel.query.first()

        if system.authentication:
            if 'token' in [i.lower() for i in request.headers.keys()] and request.headers['token'] != '':
                if request.headers['token'] != system.token:
                    if request.headers['token'] != current_app.config['SECRET_KEY']:
                        return jsonify({'authenticated': False}), 400
            else:
                return jsonify({'authenticated': False}), 400
        return f(*args, **kwargs)
    return decorated_function
