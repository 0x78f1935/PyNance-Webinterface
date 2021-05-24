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
        if bot.config.spot:
            return jsonify(list(sorted([i.to_dict(['bot_id', 'id', 'order_id', 'stop_loss', 'profit_target']) for i in bot.orders if i.spot == bot.config.spot], key=lambda x: x['updated']))[::-1])
        else:
            return jsonify(list(sorted([i.to_dict(['bot_id', 'id', 'buying', 'order_id', 'sold_for']) for i in bot.orders if i.spot == bot.config.spot], key=lambda x: x['updated']))[::-1])
