from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.balance import BalanceModel
from backend import pynance

class CandleSticksApiView(FlaskView):
    
    decorators = [ ]

    def get(self):
        symbol = request.args.get('symbol', None)
        interval = request.args.get('interval', '1m')
        if symbol is None: return jsonify([]), 200
        model = pynance.candlesticks.symbol(symbol, interval)
        return jsonify(model), 200