from flask_classful import FlaskView, route
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
from backend.models.chatterer import ChattererModel
from backend import db, pynance
from sqlalchemy import and_

from fractions import Fraction
from datetime import datetime
import math
import time


class SystemApiView(FlaskView):
    
    decorators = [ ]

    def get_x_percentage_of_y(self, x, y): return float(y / 100) * x

    def get(self):
        now = datetime.now()

        chatterer = ChattererModel.query.first()
        system = SystemModel.query.first()
        cur1 = system.currency_1
        cur2 = system.currency_2

        if not system.online: 
            chatterer.chat("CURRENTLY OFFLINE")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
                "online": False,
                "msg": "CURRENTLY OFFLINE"
            }), 200

        model = OrdersModel.query.filter(
            and_(
                OrdersModel.current == True,
                OrdersModel.currency_1 == cur1,
                OrdersModel.currency_2 == cur2,
            )).first()
        
        try:
            price_average = float(pynance.price.average(cur1+cur2).json["price"])
        except AttributeError:
            # system.online = False
            # db.session.add(system)
            # db.session.commit()
            chatterer.chat("UNKNOWN SYMBOL")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
                "online": False,
                "msg": chatterer.msg
            }), 200

        if model is None: brought_price = price_average
        else: brought_price = float(model.brought_price)

        take_profit = float(system.take_profit)  # The percentage to take as profit, cannot be higher then 99

        try:
            fees = pynance.price.fees(cur1+cur2).json['tradeFee'].pop(0)
        except AttributeError:
            # system.online = False
            # db.session.add(system)
            # db.session.commit()
            chatterer.chat("BINANCE SERVICES ARE UNAVAILABLE AT THIS TIME")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
                "online": False,
                "msg": chatterer.msg
            }), 200

        fee_maker = 1 + fees['maker'] * 100 # Maker -> Buys crypto
        fee_taker = 1 + fees['taker'] * 100 # Taker -> Sells crypto
        symbol = fees['symbol']

        exchange_info = pynance.exchange_info(symbol)
        stepSize = [ i for i in exchange_info['filters'] if i['filterType'] == 'LOT_SIZE'].pop(0)['stepSize']
        precision = int(round(-math.log(float(stepSize), 10), 0))

        balance = pynance.wallet.balance(cur1)
        balance2 = pynance.wallet.balance(cur2)

        balance_free = float(balance['free'])        # BTC
        balance_locked = float(balance['locked'])
        balance2_free = float(balance2['free'])      # USDT
        balance2_locked = float(balance2['locked'])
        current_price = float(pynance.price.asset(cur1+cur2).json['price'])

        paid_total = brought_price * balance_free
        wouldve_paid = current_price * balance_free

        if model is not None: 
            chatterer.update_price(f"{float(round(float(current_price) * float(model.quantity), 6))} - { float(round(current_price, 6)) } - { model.quantity }")
        else: chatterer.update_price(f"0.0 - { float(round(current_price, 6)) } - 0")

        sell_without_fee_lose = paid_total * fee_maker
        wanted_profit = paid_total * float(take_profit/100)
        sell_without_fee_lost_plus_profit = sell_without_fee_lose + wanted_profit
        btc_sell_price = sell_without_fee_lost_plus_profit / brought_price

        minimal_money_needed_to_buy = current_price * 0.001


        # SELLING
        if wouldve_paid > sell_without_fee_lost_plus_profit or system.panik and wouldve_paid > sell_without_fee_lose:
            chatterer.chat("SELLING")
            quantity = float(round(self.get_x_percentage_of_y(100, balance_free), precision))
            sell_order = pynance.orders.create(symbol, quantity, buy=False, order_id='test_api')
            if sell_order is not None:
                data = sell_order.json['fills'].pop(0)
                paid_total = float(data['price'])
                sell_without_fee_lose = paid_total * fee_maker
                wanted_profit = paid_total * float(take_profit/100)
                sell_without_fee_lost_plus_profit = sell_without_fee_lose + wanted_profit
                if model is not None:
                    model.update_data({
                        'current': False,
                        'sold_for': str(paid_total)
                    })
                chatterer.chat(f"SOLD: {quantity}")
            else: chatterer.chat("NOTHING TO SELL")
        else:
            # Check if we have enough money to buy
            if model is None:
                if balance2_free > minimal_money_needed_to_buy:
                    if system.panik:
                        chatterer.chat("PANIK, NO NEW BUY ORDER WILL BE PLACED")
                    else:
                        # Check if the current price is below average
                        if current_price < price_average:
                            chatterer.chat("BUYING")
                            quantity = float(f"{self.get_x_percentage_of_y(100-take_profit, balance2_free / current_price ):.{precision}f}")
                            buy_order = pynance.orders.create(symbol, quantity, order_id='test_api')
                            if buy_order is not None:
                                data = buy_order.json['fills'].pop(0)
                                brought_price = float(data['price'])
                                model = OrdersModel(
                                    symbol=symbol,
                                    currency_1=cur1,
                                    currency_2=cur2,
                                    quantity=str(quantity),
                                    brought_price=str(brought_price),
                                    fee_maker=str(fee_maker),
                                    fee_taker=str(fee_taker),
                                )
                                db.session.add(model)
                                db.session.commit()
                            chatterer.chat(f"BROUGHT: {quantity}")
                        else: chatterer.chat("CURRENT PRICE NOT BELOW AVERAGE, SKIPPING BUY ORDERS")
                else: chatterer.chat("NOT ENOUGH MONEY TO BUY")
            else: chatterer.chat("HOLDING STRONG, CURRENT PRICE TO LOW TO SELL")

        return jsonify({
            "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
            "execution_time": str(datetime.now()-now),
            "online": True,
            "msg": chatterer.msg
        }), 200