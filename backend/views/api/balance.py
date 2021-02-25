from flask_classful import FlaskView, route
from flask import jsonify, request
from sqlalchemy.sql.expression import bindparam, literal
from backend.models.balance import BalanceModel
from backend import pynance, db

class BalanceApiView(FlaskView):
    """/api/v1/balance returns the balance available in the wallet"""
    
    decorators = [ ]

    def get(self):
        """The get request fetches the data available in your wallet.
        This includes the asset name, the free amount and the locked amount.

        Args:
            The endpoint can include the argument `format`. If this is not set
            all the items in the database will return.
            If `format` is set. Only the items that are included in the format
            argument will return.

            /api/v1/balance?format=LTCBTC

            - A second argument can be provided when the `format` argument == `live`
            This second argument works the same as the `format` argument but with live data.
            The second argument is called `option`

        Returns:
            [list]: Each item in the list represents one coin and contains the keywords:
                asset, free, locked, total
        """
        result = []
        frmt = request.args.get('format', None)
        if frmt is not None and frmt not in ["live", "all"]:
            result = self._format_version([i.to_dict(['updated', 'id']) for i in BalanceModel.query.all()], limit=frmt)
        elif frmt is not None and frmt == "live":
            options = request.args.get('option', '')
            response = pynance.wallet.balance()
            if response.isSucces:
                self._save_balance_to_db(response.json['balances'], response.json['accountType'])
            if options: result = self._format_version(response.json['balances'], limit=options)
            else: result = self._format_version(response.json['balances'])
        else:
            result = self._format_version([i.to_dict(['updated', 'id']) for i in BalanceModel.query.all()])
        return jsonify(result), 200
    
    def _format_version(self, data, limit=None):
        if limit is not None:
            print(limit)
            return [
                dict(i, **{'total': str(float(i["free"]) + float(i["locked"]))})
                for i in data
                if i["asset"] in limit
            ]
        else:
            return [
                dict(i, **{'total': str(float(i["free"]) + float(i["locked"]))})
                for i in data
            ]
    
    def _save_balance_to_db(self, data, account_type):
        for item in data:
            model = BalanceModel.query.filter(BalanceModel.asset == item['asset']).first()
            if model is None:
                model = BalanceModel(account_type=account_type)
                db.session.add(model)
                db.session.commit()
            model.update_data(item)