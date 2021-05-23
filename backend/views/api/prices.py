from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

class PricesApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        """Returns prices of all symbols available"""
        symbol = None
        if request.args.keys() and 'symbol' in request.args.keys():
            symbol = request.args['symbol']
        if symbol is None: data = pynance.assets.symbols()
        else: data = pynance.assets.symbols(symbol.upper())
        if type(data.json) != list: data = [data]
        return jsonify(data.json), 200