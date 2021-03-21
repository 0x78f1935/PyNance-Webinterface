from flask_classful import FlaskView, route
from flask import jsonify, request
from backend import db, pynance
from backend.utils.auth import login_required


class SystemAPIView(FlaskView):
    
    decorators = [ login_required ]

    @route('/all', methods=['GET'])
    def all(self):
        from backend.models.system import SystemModel
        system = SystemModel.query.first()
        data = {
            **system.to_dict(['id']),
            'symbols': [i['asset'] for i in  pynance.wallet.balance()],
            'symbol': system.currency_1 + system.currency_2,
        }
        return jsonify(data), 200
    
    def get(self):
        from backend.models.system import SystemModel
        system = SystemModel.query.first()
        return jsonify(system.to_dict(['id'])), 200
   
    def post(self):
        from backend.models.system import SystemModel
        system = SystemModel.query.first()
        system.update_data(request.json)
        return jsonify(system.to_dict(['id'])), 200

    @route('/profit', methods=['POST'])
    def profit(self):
        from backend.models.orders import OrderModel
        color = 'red'
        symbol = request.json['symbol']
        total_wasted = sum([float(i.brought_price) for i in OrderModel.query.filter(OrderModel.currency_2 == symbol).all()])
        total_profit = sum([float(i.sold_for) for i in OrderModel.query.filter(OrderModel.currency_2 == symbol).all()])
        profit = total_profit-total_wasted
        if profit < 0: color = 'red'
        elif profit > 0: color = 'green'
        else: color='gray'
        return jsonify({'profit': profit, 'symbol': symbol, 'color': color}), 200
   