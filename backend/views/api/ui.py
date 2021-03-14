from flask_classful import FlaskView, route
from flask import jsonify, request, current_app

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend.models.chatterer import ChattererModel
from backend import db, pynance
from sqlalchemy import and_


class UIApiView(FlaskView):
    
    decorators = [ ]

    def update_system_without_going_offline(self, system, data):
        online = system.online
        system.update_data(data)
        system.online = online
        db.session.add(system)
        db.session.commit()
        return system

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
        symbols = [i['symbol'] for i in  pynance.price.fees(request.args.get('symbol')).json['tradeFee']]
        return jsonify({'symbols': symbols}), 200

    @route('/currency', methods=['GET'])
    def currencies(self):
        model = SystemModel.query.first()
        return jsonify({'cur1': model.currency_1, 'cur2': model.currency_2}), 200

    @route('/version', methods=['GET'])
    def version(self):
        return jsonify({'version': current_app.config['VERSION']}), 200

    @route('/maintainer', methods=['GET'])
    def maintainer(self):
        return jsonify({
            'maintainer': current_app.config['MAINTAINER'],
            'github': current_app.config['GITHUB'],
            'twitter': current_app.config['TWITTER'],
        }), 200

    @route('/profit', methods=['GET'])
    def profit(self):
        profits = [float(i.sold_for) - float(i.brought_price) * float(i.quantity) for i in OrdersModel.query.all()]
        profit = 0
        for o in profits: profit += o
        return jsonify({
            "profit": profit
        }), 200

    @route('/current_price', methods=['GET'])
    def current_price(self):
        model = ChattererModel.query.first()
        if model is not None:
            try:
                fiat, coin, quantity = model.current_price.split(' - ')
                return jsonify({'fiat': fiat, 'coin': coin, 'quantity': quantity}), 200
            except ValueError: pass
        return jsonify({'fiat': 0, 'coin': 0, 'quantity': 0}), 200

    @route('/v2/current_price', methods=['GET', 'POST'])
    def current_price_2(self):
        model = SystemModel.query.first()
        if request.method == 'GET':
            if 'cur1' in request.args and 'cur2' in request.args:
                symbol = request.args.get('cur1')+request.args.get('cur2')
                try:
                    current_price = float(round(float(pynance.price.asset(symbol).json['price']), 8))
                    average_price = pynance.price.average(symbol, model.timeinterval, model.candleinterval)
                    model = self.update_system_without_going_offline(model, {
                        'current_value': str(current_price),
                        'average_price': str(average_price),
                    })
                except AttributeError:
                    model = self.update_system_without_going_offline(model, {
                        'current_value': 'UNKNOWN',
                        'average_price': 'UNKNOWN',
                    })                
            return jsonify({
                'price': model.current_value, 
                'average_price': model.average_price,
                'timerinterval': model.timeinterval,
                'candlehistory': model.candleinterval,
            }), 200
        else:
            data = request.json
            if 'candlehistory' in data.keys():
                model = self.update_system_without_going_offline(model, {
                    'candleinterval': data['candlehistory'],
                })
            elif 'timeinterval' in data.keys():
                model = self.update_system_without_going_offline(model, {
                    'timeinterval': data['timeinterval'],
                })
            return jsonify({'timeinterval': model.timeinterval, 'candlehistory': model.candleinterval}), 200
    