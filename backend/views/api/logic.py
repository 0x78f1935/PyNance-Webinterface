from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

from datetime import datetime


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

        # Check if there is a configuration based on selected symbols
        if len(bot.config.symbols) <= 0:
            bot.chat("NO SYMBOL CONFIGURED TO TRADE")
            return jsonify({
                'online': True,
                'execution_time': str(datetime.now()-stopwatch),
            })

        # Iterate over each symbol
        for symbol in bot.config.symbols:
            bot.chat(f"CURRENT SYMBOL SELECTED - {symbol}")
            average = pynance.assets.average(symbol, bot.config.timeframe, bot.config.candle_interval)
            bot.update_average(average)

            # Check if this symbol has any open orders
            order = bot.get_order(symbol)
        
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
