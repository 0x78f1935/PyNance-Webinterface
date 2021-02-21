from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.balance import BalanceModel
from backend import pynance

class SymbolsApiView(FlaskView):
    
    decorators = [ ]

    def get(self):
        """Generates a list of coin names available

        This request has a argument `format`.
        If format is set to `coins` it will return a list of coin names
        If format is set to `tickers` it will retun a list of available tickers

        Returns:
            [string]: [Coins depending on format]
        """
        model = []
        frmt = request.args.get('format')
        if frmt == 'coins': model = [i.asset for i in BalanceModel.query.all()]
        elif frmt == 'tickers':
            tickers = pynance.get(f'{pynance.endpoint}/api/v3/ticker/bookTicker', signed=False, data={})
            if tickers.isSucces: model = [i['symbol'] for i in tickers.json]
        elif frmt == 'all':
            tickers = pynance.get(f'{pynance.endpoint}/api/v3/ticker/bookTicker', signed=False, data={})
            if tickers.isSucces: model = [i['symbol'] for i in tickers.json]
            model += [i.asset for i in BalanceModel.query.all()]
        return jsonify(list(sorted(model))), 200