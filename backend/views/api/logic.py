from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend.utils.trading import Spot, Futures
from backend import db, pynance

from datetime import datetime
import math, time


class LogicApiView(FlaskView):
    
    # decorators = [ login_required ] # TODO enable

    def get(self):
        """This method is the brain of the bot, places orders etc

        Returns:
            [dict]: {
                online: bool, indicates if the bot is online,
                execution_time: datetime, the total time it took to execute this method
            }
        """
        from backend.models.bot import BotModel
        bot = BotModel.query.first()

        if bot.config.spot:
            trade = Spot()
        else:
            trade = Futures()

        if trade.can_trade:
            for symbol in trade.get_active_symbols:
                time.sleep(1)
                print('\n\n')
                print('-'*50)
                print(symbol)
                print('-'*50)
                print('\n\n')
                can_still_trade = trade.prepare(symbol)
                if can_still_trade:
                    trade.start()

        return jsonify(trade.fetch_results())

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
