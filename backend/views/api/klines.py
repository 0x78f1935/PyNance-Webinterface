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
        order = OrdersModel.query.filter(OrdersModel.symbol == bot.status.target).first()
        if order.spot: klines = pynance.assets.klines(target, timeframe=bot.graph_type, total_candles=bot.graph_interval)
        else: klines = pynance.futures.assets.klines(target, timeframe=bot.graph_type, total_candles=bot.graph_interval)
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

    @route('/graph', methods=['GET', 'POST'])
    def set_graph(self):
        """Saves the graph view on the statistic page
        """
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        if request.method == 'POST':
            data = request.json
            bot.update_data({'online': bot.online, 'graph_type': data['graph-type'], 'graph_interval': data['graph-interval']})
        return jsonify({'graph-type': bot.graph_type, 'graph-interval': bot.graph_interval}), 200
