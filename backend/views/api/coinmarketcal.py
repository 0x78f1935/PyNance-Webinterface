from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

import requests

class CoinMarketApiView(FlaskView):
    
    decorators = [ login_required ]

    @route('/check', methods=['GET'])
    def check(self):
        url = "https://developers.coinmarketcal.com/v1/events"
        querystring = {"max":"5"}
        payload = ""
        headers = {
            'x-api-key': request.args['api-key'],
            'Accept-Encoding': "deflate, gzip",
            'Accept': "application/json"
        }
        response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
        if response.status_code == 200: 
            from backend.models.keys import KeysModel
            model = KeysModel(value="coinmarketcal", key=request.args['api-key'])
            db.session.add(model)
            db.session.commit()
            return jsonify({'error': False}), 200
        else: return jsonify({'error': True}), 400
