from flask_classful import FlaskView, route
from flask import jsonify, request

from sqlalchemy import and_

from backend.utils.auth import login_required
from datetime import datetime
from backend import db, pynance
import math


class BotAPIView(FlaskView):
    
    decorators = [ ]

    def get(self):
        from backend.models.bot import BotModel
        from backend.models.orders import OrderModel
        from backend.models.preference import PreferenceModel
        from backend.models.settings import SettingsModel
        from backend.models.system import SystemModel

        now = datetime.now()

        bot = BotModel.query.first()
        preference = PreferenceModel.query.first()
        settings = SettingsModel.query.first()
        system = SystemModel.query.first()

        if not system.online:
            bot.chat("CURRENTLY OFFLINE")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
            }), 200

        cur1 = system.currency_1
        cur2 = system.currency_2

        try:
            price_average = pynance.price.average(cur1+cur2, settings.timeframe, settings.total_candles)
        except AttributeError:
            bot.chat("UNKNOWN SYMBOL")
            system.update_data({'online': False})
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
            }), 200

        order = OrderModel.query.filter(
            and_(
                OrderModel.current == True,
                OrderModel.currency_1 == cur1,
                OrderModel.currency_2 == cur2,
            )).first()

        if order is None: work_price = price_average
        else: work_price = float(order.brought_price)

        minimal_profit = float(settings.minimal_profit)

        try:
            # Check if we can get the fees, which also allows us to check if Binance is available
            fees = pynance.price.fees(cur1+cur2).json['tradeFee'].pop(0)
        except AttributeError:
            bot.chat("BINANCE SERVICES ARE UNAVAILABLE AT THIS TIME")
            return jsonify({
                "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                "execution_time": str(datetime.now()-now),
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
        bot.update_data({'current_value': str(current_price)})

        expected_profit = float(round(float(float(work_price / 100) * minimal_profit), 8))
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

        if settings.average_distance == 0: _p = price_average
        else: _p = float(price_average - float(float(price_average/100) * settings.average_distance))
        bot.update_data({'average_price': _p})

        if bot.buying:
            fees_current_price = float(round(float(float(work_price) * fee_taker), 8))
            price_including_fee = float(round(float(float(balance_free)), 8))
            price_excluding_fee = float(round(float(float(balance_free - fees_current_price)), 8))

            if order is None:
                if preference.panik: bot.chat("PANIK ACTIVE, NO NEW BUY ORDER WILL BE PLACED")
                else:
                    if settings.average_distance == 0: price_entry = work_price
                    else: price_entry = float(work_price - float(float(work_price/100) * settings.average_distance))

                    if current_price <= price_entry:
                        bot.chat(f"BUYING {cur1}")
                        quantity = float(float(float(float(balance2_free / current_price) / 100) * float(settings.wallet_amount)))
                        buy_order = pynance.orders.create(symbol, float(round(float(quantity - float(quantity/100)), precision)), order_id='pynanceBuyOrder')
                        if buy_order is not None:
                            data = buy_order.json['fills'].pop(0)
                            brought_price = float(round(float(data['price']), 8))
                            model = OrderModel(
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
                            bot.chat(f"BROUGHT ({float(round(float(quantity), 8))}) {cur1} FOR ({float(round(float(brought_price), 8))}) {cur2}")
                            bot.update_data({'buying': False})
                        else: bot.chat(f"UNABLE TO PLACE A BUY ORDER FOR ({float(round(float(quantity), 8))}) {cur1} AT THE PRICE OF ({float(round(float(current_price), 8))}) {cur2}")
                    else: bot.chat(f"CURRENT {cur1} PRICE ({float(round(float(current_price), 8))}) NOT AT BUY TARGET ({float(round(float(price_entry), 8))}), SKIPPING BUY ORDER")
            else:
                bot.update_data({'buying': False})
                bot.chat("NOT ENOUGH MONEY TO PLACE A BUY ORDER")

        else:
            fees_current_price = float(round(float(float(work_price) * fee_taker), 8))
            price_including_fee = float(round(float(float(balance2_free)), 8))
            price_excluding_fee = float(round(float(float(balance2_free - fees_current_price)), 8))

            if order is None:
                bot.chat("No coin available to sell, you seem to be out of stock!")
                bot.update_data({'buying': True})
                return jsonify({
                    "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
                    "execution_time": str(datetime.now()-now),
                }), 200

            quantity = float(round(float(order.quantity), precision))
            sell_target = float(round(float(float(total_profit_on_each_coin * quantity) + float(float(total_profit_on_each_coin * quantity) * fee_taker)), 8))

            previous_price_order = float(round(float(work_price * quantity), 8))
            expected_total_profit = float(round(float(sell_target - previous_price_order), 8))
            total_fomo_price = float(round(float(work_price + fees_current_price), 8))
            fomo_price = float(round(float(float(total_fomo_price * quantity) + float(float(total_fomo_price * quantity) * fee_taker)), 8))

            if preference.panik: bot.chat(f"({quantity}) {cur1} IS ({float(round(float(current_price * quantity), 8))}) {cur2} WORTH - TRYING TO SELL FOR ({fomo_price}) {cur2}")
            else: bot.chat(f"({quantity}) {cur1} IS ({float(round(float(current_price * quantity), 8))}) {cur2} WORTH - TRYING TO SELL FOR ({sell_target}) {cur2}")

            if current_price > total_profit_on_each_coin or preference.panik and current_price > total_fomo_price:
                bot.chat(f"SELLING {cur1}")
                sell_order = pynance.orders.create(symbol, float(round(float(quantity - float(float(quantity/100)*2.5)), precision)), buy=False, order_id='pynanceSellEntry')
                if sell_order is not None:
                    sold_price = float(round(float(current_price * quantity), 8))
                    if order is not None:
                        order.update_data({
                            'current': False,
                            'sold_for': str(sold_price)
                        })
                        bot.chat(f"SOLD ({float(round(float(quantity), 8))}) {cur1} FOR AN AMAZING ({float(round(float(sold_price), 8))}) {cur2}")
                        bot.update_data({'buying': True})
                else: bot.chat(f"UNABLE TO PLACE A SELL ORDER FOR ({float(round(float(quantity), 8))}) {cur1}")

        return jsonify({
            "date": str(datetime.now().strftime('%d-%m-%y %H:%M:%S')),
            "execution_time": str(datetime.now()-now),
        }), 200

    @route('/msg', methods=['GET'])
    def msg(self):
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        return jsonify(bot.to_dict(['id'])), 200

    def post(self):
        from backend.models.bot import BotModel
        bot = BotModel.query.first()
        bot.update_data(request.json)
        return jsonify(bot.to_dict(['id'])), 200

    @route('/current_price', methods=['GET', 'POST'])
    def current_price(self):
        from backend.models.bot import BotModel
        from backend.models.settings import SettingsModel
        bot = BotModel.query.first()
        settings = SettingsModel.query.first()
        if 'cur1' in request.args and 'cur2' in request.args:
            symbol = request.args.get('cur1')+request.args.get('cur2')
            try:
                current_price = float(round(float(pynance.price.asset(symbol).json['price']), 8))
                work_price = pynance.price.average(symbol, settings.timeframe, settings.total_candles)

                if settings.average_distance == 0: average_price = work_price
                else: average_price = float(work_price - float(float(work_price/100) * settings.average_distance))

                bot.update_data({
                    'current_value': current_price,
                    'average_price': average_price,
                })
            except (AttributeError, KeyError):
                bot.update_data({
                    'current_value': 0,
                    'average_price': 0,
                })                
        return jsonify({
            'current_value': bot.current_value,
            'average_price': bot.average_price,
        }), 200
