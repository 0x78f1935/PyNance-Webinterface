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

    @route('/events', methods=['POST'])
    def events(self):
        from backend.models.keys import KeysModel
        model = KeysModel.query.filter(KeysModel.value == 'coinmarketcal').first()
        if model is not None:
            url = "https://developers.coinmarketcal.com/v1/events"
            querystring = {
                "max": request.json['max'],
                "page": request.json['page'],
                "sortBy": request.json['sortBy'],
                "showOnly": request.json['showOnly']
            }
            payload = ""
            headers = {
                'x-api-key': model.key,
                'Accept-Encoding': "deflate, gzip",
                'Accept': "application/json"
            }
            response = requests.request("GET", url, data=payload, headers=headers, params=querystring)
            data = response.json()
            return jsonify({
                'pagecount': data['_metadata']['page_count'],
                'total_items': data['_metadata']['total_count'],
                'events': [
                    {
                        'title': i['title']['en'] if 'title' in i.keys() and 'en' in i['title'].keys() else '',
                        'coins': i['coins'] if 'coins' in i.keys() else [],
                        'date_event': i['date_event'] if 'date_event' in i.keys() else '',
                        'can_occur_before': i['can_occur_before'] if 'can_occur_before' in i.keys() else False,
                        'created': i['created_date'] if 'created_date' in i.keys() else '',
                        'categories': [y['name'] for y in i['categories']] if 'categories' in i.keys() else [],
                        'proof': i['proof'] if 'proof' in i.keys() else '',
                        'source': i['source'] if 'source' in i.keys() else '',

                    } for i in data['body']
                ]
            }), 200

