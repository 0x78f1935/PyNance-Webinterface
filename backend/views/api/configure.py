from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend import db, pynance
from sqlalchemy import and_

import operator


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

    @route('/cur1', methods=['POST'])
    def cur1(self):
        model = SystemModel.query.first()
        model.currency_1 = request.json['cur']
        db.session.add(model)
        db.session.commit()
        return jsonify({'cur1': model.currency_1, 'cur2': model.currency_2}), 200

    @route('/cur2', methods=['POST'])
    def cur2(self):
        model = SystemModel.query.first()
        model.currency_2 = request.json['cur']
        db.session.add(model)
        db.session.commit()
        return jsonify({'cur1': model.currency_1, 'cur2': model.currency_2}), 200

    @route('/panik', methods=['POST', 'GET'])
    def panik(self):
        model = SystemModel.query.first()
        if request.method == 'POST':
            online = model.online # Prevents model to set itself to false
            model.update_data(request.json)
            model.online = online
            db.session.add(model)
            db.session.commit()
            return jsonify({'panik': model.panik}), 200
        else:
            return jsonify({'panik': model.panik}), 200

    @route('/only_dip', methods=['POST'])
    def only_dip(self):
        model = SystemModel.query.first()
        model.update_data({'only_dip': not request.json['dip']})
        return jsonify({'dip': model.only_dip}), 200
