from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

from datetime import datetime
import math


class LogicApiView(FlaskView):
    
    # TODO enable
    # decorators = [ login_required ]

    def get(self):
        """This method is the brain of the bot, places orders etc

        Returns:
            [dict]: {
                online: bool, indicates if the bot is online,
                execution_time: datetime, the total time it took to execute this method
            }
        """
        stopwatch = datetime.now()

        from backend.models.bot import BotModel
        bot = BotModel.query.first()

        # Check if bot is online
        if not bot.online:
            bot.chat("CURRENTLY OFFLINE")
            return jsonify({
                'online': False,
                'execution_time': str(datetime.now()-stopwatch),
            })
        
        binance_status = pynance.system.maintenance()
        if binance_status.json['status'] != 0:
            bot.chat("BINANCE IS CURRENTLY UNAVAILABLE")
            return jsonify({
                'online': True,
                'execution_time': str(datetime.now()-stopwatch),
            })

        # Check if there is a configuration based on selected symbols
        if len(bot.config.symbols) <= 0:
            bot.chat("NO SYMBOL CONFIGURED TO TRADE")
            return jsonify({
                'online': True,
                'execution_time': str(datetime.now()-stopwatch),
            })

        # Iterate over each symbol
        for symbol in bot.config.symbols:
            # Update the current average
            bot.chat(f"CURRENT SYMBOL SELECTED - {symbol}")
            average = pynance.assets.average(symbol, bot.config.timeframe, bot.config.candle_interval)
            if bot.config.below_average > 0: average = float(average - float(float(average/100) * bot.config.below_average))
            bot.update_average(average)

            # Check if this symbol has any open orders
            order = bot.get_order(symbol)

            # Check if we are buying or if we are selling
            # One full cycle if buying asset B and selling asset B for asset A
            if order.buying:
                minimal_profit = bot.config.profit_margin
                asset_fees = pynance.assets.fees(symbol)  # makerCommission | takerCommission
                asset_exchange_info = pynance.assets.exchange_info(symbol).json['symbols'].pop(0)
                # Calculate the precision size of the symbol
                stepSize = [ i for i in asset_exchange_info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['stepSize']
                precision = int(round(-math.log(float(stepSize), 10), 0))
                # Get the asset names
                base_asset = asset_exchange_info['baseAsset']
                quote_asset = asset_exchange_info['quoteAsset']

                # Check for each asset selected what we have available in the wallet
                balance = pynance.wallet.balance()
                base_balance = [i for i in balance.json if i['coin'] == base_asset][0]
                balance_free = float(round(float(base_balance['free']), 8))
                if balance_free < 10:
                    bot.chat(f"NOT ENOUGH {base_asset} TO BUY - {quote_asset} - {balance_free} {base_asset} AVAILABLE NEED 10 {base_asset}")
                    return jsonify({
                        'online': True,
                        'execution_time': str(datetime.now()-stopwatch),
                    })
                

                print(1)

        
        return jsonify({
            'online': True,
            'execution_time': str(datetime.now()-stopwatch),
        })

    @route('toggle', methods=['POST', 'GET'])
    def toggle(self):
        """Toggles the bot offline and online
        """
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        if request.method == 'POST':
            option = request.json['online']
            bot.update_data({'online': option})
        return jsonify({'online': bot.online})

    @route('systembar', methods=['GET'])
    def systembar(self):
        """Gets called often to retrieve the status of the bot
        """
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        return jsonify(bot.status.to_dict(['id']))
