from flask_classful import FlaskView
from flask import jsonify

from backend import pynance, db
from backend.models.balance import BalanceModel


class TestPageView(FlaskView):
    
    decorators = [ ]

    def get(self):
        trades = pynance.get(
            f'{pynance.endpoint}/api/v3/allOrders',
            signed=True,
            data={
                "symbol": "LTCBTC"
            }
        )
        # for item in response.json['balances']:
        #     model = BalanceModel.query.filter(BalanceModel.asset == item['asset']).first()
        #     if(model is None):
        #         model = BalanceModel(account_type=response.json['accountType'])
        #         db.session.add(model)
        #         db.session.commit()
        #     model.update_data(item)

        balance = pynance.get(f'{pynance.endpoint}/api/v3/account', signed=True, data={})

        tickers = pynance.get(f'{pynance.endpoint}/api/v3/ticker/bookTicker', signed=False, data={})

        return jsonify('success!'), 200