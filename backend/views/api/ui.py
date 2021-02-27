from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend.models.chatterer import ChattererModel
from backend import db, pynance
from sqlalchemy import and_


class UIApiView(FlaskView):
    
    decorators = [ ]

    @route('/knightrider', methods=['GET'])
    def knightrider(self):
        model = ChattererModel.query.first()
        return jsonify({'chatterer': model.msg}), 200

    @route('/online', methods=['GET'])
    def is_online(self):
        model = SystemModel.query.first()
        return jsonify({'online': model.online}), 200