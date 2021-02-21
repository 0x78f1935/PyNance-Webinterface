from flask_classful import FlaskView
from flask import jsonify

from backend import pynance, db
from backend.models.balance import BalanceModel


class BalanceCrontabView(FlaskView):
    
    decorators = [ ]

    def get(self):
        response = pynance.wallet.balance()
        for item in response.json['balances']:
            model = BalanceModel.query.filter(BalanceModel.asset == item['asset']).first()
            if(model is None):
                model = BalanceModel(account_type=response.json['accountType'])
                db.session.add(model)
                db.session.commit()
            model.update_data(item)

        return jsonify('success!'), 200