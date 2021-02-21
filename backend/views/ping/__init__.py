from flask_classful import FlaskView
from flask import jsonify


class PingPageView(FlaskView):
    
    decorators = [ ]

    def get(self):
        return jsonify('pong!')