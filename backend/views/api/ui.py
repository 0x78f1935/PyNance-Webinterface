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
    
    @route('/symbols', methods=['GET'])
    def symbols(self):
        symbols = [i['asset'] for i in  pynance.wallet.balance()]
        return jsonify({'symbols': symbols}), 200

    @route('/symbols_sets', methods=['GET'])
    def symbols_sets(self):
        symbols = [i['symbol'] for i in  pynance.price.fees().json['tradeFee']]
        return jsonify({'symbols': symbols}), 200

    @route('/currency', methods=['GET'])
    def currencies(self):
        model = SystemModel.query.first()
        return jsonify({'cur1': model.currency_1, 'cur2': model.currency_2}), 200

