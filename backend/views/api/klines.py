from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance


class KlinesApiView(FlaskView):
    
    decorators = [ login_required ]

    def get(self):
        from backend.models.config import ConfigModel
        config = ConfigModel.query.first()
        klines = pynance.assets.klines('LTCUSDT', timeframe=config.timeframe, total_candles=config.candle_interval)
        # TODO make data dynamic
        return jsonify({
            'klines': klines, 
            'target': 'LTCUSDT', 
            'current_target': 270.00, 
            'target_type': 'BUY TARGET',
            'status': {
                'target': 'LTCUSDT', 
                'current_target': 270.00, 
                'target_type': 'buy',
            }
        })
