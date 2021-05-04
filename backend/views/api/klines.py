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
        target = bot.status.target
        if target == "NO TARGET": target = "ADAUSDT"
        klines = pynance.assets.klines(target, timeframe=bot.config.timeframe, total_candles=bot.config.candle_interval)
        order = OrdersModel.query.filter(OrdersModel.symbol == bot.status.target).first()
        target_type = 'WAITING FOR CONFIG'
        trade_type = 'NONE'
        target_type_status = 'NO TRADE CONFIG'
        if order is not None:
            target_type = 'BUY TARGET' if order.buying else 'SELL TARGET'
            trade_type = 'SPOT' if order.spot else 'FUTURE'
            target_type_status = 'buy' if order.buying else 'selling'

        return jsonify({
            'klines': klines, 
            'target': bot.status.target,
            'current_target': bot.status.average, 
            'target_type': target_type,
            'trade_type': trade_type,
            'status': {
                'target': bot.status.target, 
                'current_target': bot.status.average, 
                'target_type': target_type_status,
            }
        })
