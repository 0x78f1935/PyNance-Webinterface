from flask_classful import FlaskView, route
from flask import jsonify, request
from backend.utils.auth import login_required

from backend import db, pynance


class OrdersAPIView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.orders import OrderModel
        orders = [i.to_dict(['id', 'current', 'currency_1', 'currency_2', 'fee_maker', 'fee_taker']) for i in OrderModel.query.all()]
        return jsonify(orders), 200
