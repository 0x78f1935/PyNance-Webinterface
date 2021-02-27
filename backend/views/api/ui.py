from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend import db, pynance
from sqlalchemy import and_


class UIApiView(FlaskView):
    
    decorators = [ ]

    @route('/knightrider', methods=['GET'])
    def knightrider(self):
        model = SystemModel.query.first()
        return jsonify({'chatterer': model.chatterer}), 200