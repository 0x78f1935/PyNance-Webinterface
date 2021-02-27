from flask_classful import FlaskView
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend import db, pynance
from sqlalchemy import and_


class OrdersApiView(FlaskView):
    
    decorators = [ ]

    def get(self):
        data = [i.to_dict(['id']) for i in OrdersModel.query.all()]
        return jsonify(data), 200