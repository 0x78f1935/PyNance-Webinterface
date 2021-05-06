from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

class WalletApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        """Returns wallet balance"""
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        if bot.config.spot: data = pynance.wallet.balance()
        else: data = pynance.futures.wallet.balance()
        return jsonify({
            'status': data.response_info['status_code'],
            'wallet': data.json
        }), 200
