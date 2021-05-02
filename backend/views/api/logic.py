from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance


class LogicApiView(FlaskView):
    
    # TODO enable
    # decorators = [ login_required ]

    def get(self):
        return jsonify({})

    @route('toggle', methods=['POST'])
    def toggle(self):
        """Toggles the bot offline and online
        """
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        option = request.json['online']
        bot.update_data({'online': option})
        return jsonify({'online': bot.online})
