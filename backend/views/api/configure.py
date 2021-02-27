from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend import db, pynance
from sqlalchemy import and_


class ConfigureApiView(FlaskView):
    
    decorators = [ ]

    @route('/take_profit', methods=['GET'])
    def take_profit(self):
        model = SystemModel.query.first()
        return jsonify({'take_profit': int(model.take_profit)}), 200

    @route('/take_profit', methods=['POST'])
    def set_take_profit(self):
        model = SystemModel.query.first()
        if model.take_profit != str(request.json['tp']):
            model.take_profit = str(request.json['tp'])
            db.session.add(model)
            db.session.commit()
        return jsonify({'take_profit': int(model.take_profit)}), 200
    
    @route('/online', methods=['GET'])
    def toggle_online(self):
        model = SystemModel.query.first()
        model.online = False if model.online else True
        db.session.add(model)
        db.session.commit()
        return jsonify('success'), 200
