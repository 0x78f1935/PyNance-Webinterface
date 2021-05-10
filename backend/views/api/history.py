from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance


class HistoryApiView(FlaskView):
    
    decorators = [ login_required ]

    @route('/orders', methods=['GET'])
    def get(self):
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        return jsonify([i.to_dict(['bot_id', 'id', 'buying', 'order_id']) for i in bot.orders if i.spot == bot.config.spot])
