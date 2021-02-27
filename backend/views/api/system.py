from flask_classful import FlaskView
from flask import jsonify, request

from backend.models.orders import OrdersModel
from backend.models.system import SystemModel
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

        system = SystemModel.query.first()
        cur1 = system.currency_1
        cur2 = system.currency_2

        if not system.online: return jsonify({
            "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
            "execution_time": str(datetime.now()-now),
            "online": False,
            "msg": "Currently not running ..."
        }), 200

        model = OrdersModel.query.filter(
            and_(
                OrdersModel.current == True,
                OrdersModel.currency_1 == cur1,
                OrdersModel.currency_2 == cur2,
            )).first()
        
        price_average = float(pynance.price.average(cur1+cur2).json["price"])
        if model is None: brought_price = price_average
        else: brought_price = float(model.brought_price)

        take_profit = float(system.take_profit)  # The percentage to take as profit, cannot be higher then 99

        fees = pynance.price.fees(cur1+cur2).json['tradeFee'].pop(0)

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

        sell_without_fee_lose = paid_total * fee_maker
        wanted_profit = paid_total * float(take_profit/100)
        sell_without_fee_lost_plus_profit = sell_without_fee_lose + wanted_profit
        btc_sell_price = sell_without_fee_lost_plus_profit / brought_price

        minimal_money_needed_to_buy = current_price * 0.001


        # SELLING
        if wouldve_paid > sell_without_fee_lost_plus_profit:
            system.chat("SELLING")
            quantity = float(round(self.get_x_percentage_of_y(100, balance_free), precision))
            sell_order = pynance.orders.create(symbol, quantity, False, order_id='test_api')
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
                system.chat(f"SOLD: {quantity}")
            else: system.chat("NOTHING TO SELL")
        else:
            # Check if we have enough money to buy
            if model is None:
                if balance2_free > minimal_money_needed_to_buy:
                    # Check if the current price is below average
                    if current_price < price_average:
                        system.chat("BUYING")
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
                            )
                            db.session.add(model)
                            db.session.commit()
                        system.chat(f"BROUGHT: {quantity}")
                else:
                    system.chat("NOT ENOUGH MONEY TO BUY")
            else: system.chat("HOLDING STRONG, PRICE TO LOW TO SELL")

        return jsonify({
            "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
            "execution_time": str(datetime.now()-now),
            "online": True,
            "msg": system.chatterer
        }), 200