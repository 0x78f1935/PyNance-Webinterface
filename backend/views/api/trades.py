from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

class TradesApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        """Loads the current configuration and loads it into the store in the frontend.
        The user can change the values and save the changes to confirm the changes.

        Returns:
            [dict]: {
                'assets': [A list of available assets from Binance],
                'symbols': [The selected symbols to trade],
                'symbols-choices': [A list of available symbols from Binance],
                'timeframe-choices': [A list of available graph time frames],
                'timeframe': Returns a string representing the selected timeframe,
                'candle-interval': Returns an integer which represents the selected candle-interval,
                'wallet-amount': Returns an integer which is the total amount of % available free coins to use when placing buy orders,
                'below-average': Returns an integer which pushes the lowest average x% lower,
                'profit-margin': Returns an integer which represent the profit % used for sell orders,
                'profit-as': Is used to calculate all profit as the selected asset
            }
        """
        symbols = [i['symbol'] for i in pynance.assets.symbols().json]
        assets = [i['coin'] for i in pynance.wallet.balance().json]
        from backend.models.config import ConfigModel
        config = ConfigModel.query.first()
        return jsonify({
            'sandbox': config.sandbox,
            'assets': assets,
            'symbols': config.symbols,
            'symbols-choices': symbols,
            'timeframe-choices': ['1m', '3m', '5m', '15m', '30m', '1h', '2h', '4h', '6h', '8h', '12h', '1d', '3d', '1w', '1M'],
            'timeframe': config.timeframe,
            'candle-interval': config.candle_interval,
            'wallet-amount': config.wallet_amount,
            'below-average': config.below_average,
            'profit-margin': config.profit_margin,
            'profit-as': config.profit_as,
            'spot': config.spot,
            'default-stop-loss': config.default_stop_loss,
            'total-TP': config.total_tp,            
            'in-green': config.in_green,
            'move-stop-loss': config.move_stop_loss,
            'take-profit': config.take_profit,
            'use-average': config.use_average,
            'expected-leverage': config.expected_leverage,
            'volume-timeframe': config.volume_timeframe,
            'total-volume': config.total_volume,
            'margin-type': config.margin_type,
        }), 200

    def post(self):
        """Saves the users trade configuration which is used while trading
        """
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        bot.update_data({'online': False})
        data = request.json
        from backend.models.config import ConfigModel
        config = ConfigModel.query.first()
        config.update_data({**data})
        [i.set_active(False) for i in bot.orders if i.symbol not in config.symbols]
        [i.set_active(True) for i in bot.orders if i.symbol in config.symbols and i.sold_for == 0]
        if not config.sandbox: config.remove_sandbox()
        return jsonify({}), 200
