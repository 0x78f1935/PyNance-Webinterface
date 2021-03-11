from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend import db, pynance
from sqlalchemy import and_


class OrdersApiView(FlaskView):
    
    decorators = [ ]

    @route('/', methods=['GET'])
    def get(self):
        model = SystemModel.query.first()
        take_profit = float(model.take_profit)
        data = [i.to_dict(['id']) for i in OrdersModel.query.order_by(OrdersModel.id.desc()).all()]
        results = []
        for item in data:
            order_item = {}
            order_item["Symbol"] = item["symbol"]
            order_item["Active"] = str(bool(item["current"])).capitalize() if str(model.currency_1 + model.currency_2) in order_item["Symbol"] else "False"
            order_item["quantity"] = float(item["quantity"])
            order_item["paid_total"] = float(item["brought_price"]) * order_item["quantity"]
            order_item["total_fee_paid"] = float(item["fee_taker"]) / order_item["paid_total"]
            order_item["fees_amount"] = order_item["paid_total"] - order_item["total_fee_paid"]
            order_item["wanted_profit"] = order_item["paid_total"] * float(take_profit/100)
            order_item["sellprice_without_loss_on_fee_plus_profit"] = order_item["paid_total"] + order_item["wanted_profit"]
            order_item["sold_for"] = item["sold_for"]

            results.append(order_item)
        return jsonify(results), 200