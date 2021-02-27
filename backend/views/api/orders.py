from flask_classful import FlaskView
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend import db, pynance
from sqlalchemy import and_


class OrdersApiView(FlaskView):
    
    decorators = [ ]

    def get(self):
        model = SystemModel.query.first()
        data = [i.to_dict(['id']) for i in OrdersModel.query.all()]
        for item in data:
            paid_total = float(item["brought_price"]) * float(item["quantity"])
            sell_without_fee_lose = paid_total * float(item["fee_maker"])
            wanted_profit = paid_total * float(float(model.take_profit)/100)
            sell_without_fee_lost_plus_profit = sell_without_fee_lose + wanted_profit
            item["paid"] = paid_total
            item["sell_without_fee_lose"] = sell_without_fee_lose
            item["sell_without_fee_lost_plus_profit"] = sell_without_fee_lost_plus_profit
            del item['fee_taker']
            del item['fee_maker']
        return jsonify(data), 200