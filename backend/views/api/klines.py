from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route
from sqlalchemy import and_
from backend.utils.auth import login_required
from backend import db, pynance


class KlinesApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.bot import BotModel
        from backend.models.orders import OrdersModel
        bot = BotModel.query.first()

        order = OrdersModel.query.filter(and_(
            OrdersModel.symbol==bot.status.target,
            OrdersModel.spot==bot.config.spot,
            OrdersModel.sandbox==bot.config.sandbox,
            OrdersModel.active==True
        )).first()

        response_data = {
            'target_type': 'WAITING FOR ONLINE STATUS',
            'trade_type': 'NONE',
            'target_type_status': 'NOT RUNNING',
        }
        kline_headers = ["Open time", "Open", "High", "Low", "Close", "Volume", "Close time", "Quote asset volume", "Number of trades", "Taker buy base asset volume", "Taker buy quote asset volume", "Ignore"]
        if order is None: response_data['order'] = False
        else: 
            response_data['order'] = True
            response_data['symbol'] = order.symbol
            response_data['price_target'] = bot.status.average
            if order.spot:
                response_data['trade_type'] = 'SPOT'
                response_data['target_type'] = 'BUYING' if order.buying else 'SELLING'
                klines_data = list(sorted(
                    pynance.assets.klines(order.symbol, timeframe=bot.graph_type, total_candles=bot.graph_interval),
                    key=lambda x: x[0]
                ))
                klines_data.insert(0, kline_headers)
                response_data['klines'] = klines_data
            else:
                response_data['trade_type'] = 'FUTURES'
                response_data['target_type'] = 'PLACED' if order.stop_loss > 0 else 'PROCESSING'
                response_data['stop_loss'] = order.stop_loss
                response_data['take_profit'] = order.profit_target
                response_data['position'] = 'LONG' if order.buying else 'SHORT'
                klines_data = list(sorted(
                    pynance.futures.assets.klines(order.symbol, timeframe=bot.graph_type, total_candles=bot.graph_interval),
                    key=lambda x: x[0]
                ))
                klines_data.insert(0, kline_headers)
                response_data['klines'] = klines_data

        return jsonify(response_data)

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
