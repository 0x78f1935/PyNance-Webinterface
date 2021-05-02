from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance


class KlinesApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.bot import BotModel
        from backend.models.orders import OrdersModel
        bot = BotModel.query.first()
        klines = pynance.assets.klines('LTCUSDT', timeframe=bot.config.timeframe, total_candles=bot.config.candle_interval)
        order = OrdersModel.query.filter(OrdersModel.symbol == bot.status.target).first()
        return jsonify({
            'klines': klines, 
            'target': bot.status.target,
            'current_target': bot.status.average, 
            'target_type': 'BUY TARGET' if order.buying else 'SELL TARGET',
            'status': {
                'target': bot.status.target, 
                'current_target': bot.status.average, 
                'target_type': 'buy' if order.buying else 'selling',
            }
        })
