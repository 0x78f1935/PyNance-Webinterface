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

    def update_system_without_going_offline(self, system, data):
        online = system.online
        system.update_data(data)
        system.online = online
        db.session.add(system)
        db.session.commit()
        return system

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
            chatterer.chat("UNKNOWN SYMBOL")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
                "online": False,
                "msg": chatterer.msg
            }), 200

        # The work price is or the average price, or the price which we brought for
        if model is None: work_price = price_average
        else:  work_price = float(model.brought_price)
        # The percentage to take as profit, cannot be higher then 99
        take_profit = float(system.take_profit)

        try:
            # Check if we can get the fees, which also allows us to check if Binance is available
            fees = pynance.price.fees(cur1+cur2).json['tradeFee'].pop(0)
        except AttributeError:
            chatterer.chat("BINANCE SERVICES ARE UNAVAILABLE AT THIS TIME")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
                "online": False,
                "msg": chatterer.msg
            }), 200

        # Get the fees from the response
        fee_maker = fees['maker'] # Maker -> Buys crypto
        fee_taker = fees['taker'] # Taker -> Sells crypto
        symbol = fees['symbol']

        # Get information about the selected symbol
        exchange_info = pynance.exchange_info(symbol)
        stepSize = [ i for i in exchange_info['filters'] if i['filterType'] == 'LOT_SIZE'].pop(0)['stepSize']
        precision = int(round(-math.log(float(stepSize), 10), 0))

        # Check for each currency selected what we have available in the wallet
        balance = pynance.wallet.balance(cur1)  # BTC
        balance2 = pynance.wallet.balance(cur2)  # USDT

        # Each wallet has free amounts and locked amounts, locked is not usable.
        balance_free = float(round(float(balance['free']), 8))        # BTC
        balance_locked = float(round(float(balance['locked']), 8))
        balance2_free = float(round(float(balance2['free']), 8))      # USDT
        balance2_locked = float(round(float(balance2['locked']), 8))
        current_price = float(round(float(pynance.price.asset(cur1+cur2).json['price']), 8))
        # Register the current value
        system = self.update_system_without_going_offline(system, {'current_value': str(current_price)})

        expected_profit = float(round(float(float(work_price / 100) * take_profit), 8))
        total_profit_on_each_coin = float(round(float(work_price + expected_profit), 8)) # * quantity == sell_target

        # Debug stuff
        # print(f"The work price is: {work_price}")
        # print(f"Take profit: {take_profit}%")
        # print(f"Fees limit sell / buy: {fee_maker}")
        # print(f"Fees market sell / buy: {fee_taker}")
        # print(f"Balance {cur1} -> free {balance_free}, locked {balance_locked}")
        # print(f"Balance2 {cur2} -> free {balance2_free}, locked {balance2_locked}")
        # print(f"Current price {current_price}")
        # print(f"Expected profit: {expected_profit}")
        # print(f"Buying? : {system.buying}")

        if system.buying:
            fees_current_price = float(round(float(float(work_price) * fee_taker), 8))
            price_including_fee = float(round(float(float(balance_free)), 8))
            price_excluding_fee = float(round(float(float(balance_free - fees_current_price)), 8))

            if model is None:
                if system.panik: chatterer.chat("PANIK ACTIVE, NO NEW BUY ORDER WILL BE PLACED")
                else:
                    if system.only_dip: price_entry = float(work_price - float(expected_profit))
                    else: price_entry = float(work_price - float(expected_profit / 2))

                    if current_price <= price_entry:
                        chatterer.chat(f"BUYING {cur1}")
                        quantity = float(float(float(float(balance2_free / current_price) / 100) * float(system.total_entry)))
                        buy_order = pynance.orders.create(symbol, float(round(float(quantity - float(quantity/100)), precision)), order_id='test_api')
                        if buy_order is not None:
                            data = buy_order.json['fills'].pop(0)
                            brought_price = float(round(float(data['price']), 8))
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
                            chatterer.chat(f"BROUGHT {quantity} {cur1} FOR {brought_price} {cur2}")
                            system = self.update_system_without_going_offline(system, {'buying': False}) # Reset state
                        else: chatterer.chat(f"UNABLE TO PLACE A BUY ORDER FOR {quantity} {cur1}")
                    else: chatterer.chat(f"CURRENT {cur1} PRICE ({current_price}) NOT AT BUY TARGET ({price_entry}), SKIPPING BUY ORDER")
            else:
                system = self.update_system_without_going_offline(system, {'buying': False}) # Reset state
                chatterer.chat("NOT ENOUGH MONEY TO PLACE A BUY ORDER")
        else:
            fees_current_price = float(round(float(float(work_price) * fee_taker), 8))
            price_including_fee = float(round(float(float(balance2_free)), 8))
            price_excluding_fee = float(round(float(float(balance2_free - fees_current_price)), 8))

            if model is None:
                chatterer.chat("No coin available to sell, you seem to be out of stock!")
                system = self.update_system_without_going_offline(system, {'buying': True}) # Reset state
                return jsonify({
                    "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                    "execution_time": str(datetime.now()-now),
                    "online": True,
                    "msg": chatterer.msg
                }), 200

            quantity = float(round(float(model.quantity), precision))
            sell_target = float(round(float(float(total_profit_on_each_coin * quantity) + float(float(total_profit_on_each_coin * quantity) * fee_taker)), 8))

            previous_price_order = float(round(float(work_price * quantity), 8))
            expected_total_profit = float(round(float(sell_target - previous_price_order), 8))
            total_fomo_price = float(round(float(work_price + fees_current_price), 8))
            fomo_price = float(round(float(float(total_fomo_price * quantity) + float(float(total_fomo_price * quantity) * fee_taker)), 8))

            if system.panik: chatterer.chat(f"{quantity} {cur1} IS {previous_price_order} {cur2} WORTH - TRYING TO SELL FOR {fomo_price} {cur2}")
            else: chatterer.chat(f"{quantity} {cur1} IS {previous_price_order} {cur2} WORTH - TRYING TO SELL FOR {sell_target} {cur2}")

            if current_price > total_profit_on_each_coin or system.panik and current_price > total_fomo_price:
                chatterer.chat(f"SELLING {cur1}")
                sell_order = pynance.orders.create(symbol, float(round(float(quantity - float(quantity/100)), precision)), buy=False, order_id='test_api')
                if sell_order is not None:
                    sold_price = float(round(float(current_price * quantity), 8))
                    if model is not None:
                        model.update_data({
                            'current': False,
                            'sold_for': str(sold_price)
                        })
                        chatterer.chat(f"SOLD {quantity} {cur1} FOR AN AMAZING {sold_price} {cur2}")
                        system = self.update_system_without_going_offline(system, {'buying': True}) # Reset state
                else: chatterer.chat(f"UNABLE TO PLACE A SELL ORDER FOR {quantity} {cur1}")

        return jsonify({
            "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
            "execution_time": str(datetime.now()-now),
            "online": True,
            "msg": chatterer.msg
        }), 200