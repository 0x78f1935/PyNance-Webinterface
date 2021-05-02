from flask import render_template, jsonify, current_app, request
from flask_classful import FlaskView, route

from backend.utils.auth import login_required
from backend import db, pynance

from datetime import datetime
import math


class LogicApiView(FlaskView):
    
    # TODO enable
    # decorators = [ login_required ]

    def get(self):
        """This method is the brain of the bot, places orders etc

        Returns:
            [dict]: {
                online: bool, indicates if the bot is online,
                execution_time: datetime, the total time it took to execute this method
            }
        """
        stopwatch = datetime.now()

        from backend.models.bot import BotModel
        bot = BotModel.query.first()

        # Check if bot is online
        if not bot.online:
            bot.chat("CURRENTLY OFFLINE")
            return jsonify({
                'online': False,
                'execution_time': str(datetime.now()-stopwatch),
            })
        
        binance_status = pynance.system.maintenance()
        if binance_status.json['status'] != 0:
            bot.chat("BINANCE IS CURRENTLY UNAVAILABLE")
            return jsonify({
                'online': True,
                'execution_time': str(datetime.now()-stopwatch),
            })

        # Check if there is a configuration based on selected symbols
        if len(bot.config.symbols) <= 0:
            bot.chat("NO SYMBOL CONFIGURED TO TRADE")
            return jsonify({
                'online': True,
                'execution_time': str(datetime.now()-stopwatch),
            })

        # Iterate over each symbol
        for symbol in [i.symbol for i in bot.orders if i.active]:
            print('\n\n')
            print('-'*50)
            print(symbol)
            print('-'*50)
            print('\n\n')

            bot.update_target(symbol)
            # Update the current average
            bot.chat(f"CURRENT SYMBOL SELECTED - {symbol}")
            average = pynance.assets.average(symbol, bot.config.timeframe, bot.config.candle_interval)
            if bot.config.below_average > 0: average = float(average - float(float(average/100) * bot.config.below_average))
            bot.update_average(average)

            # Check if this symbol has any open orders
            order = bot.get_order(symbol)

            # Get exhange data
            asset_exchange_info = pynance.assets.exchange_info(symbol).json['symbols'].pop(0)
            # Calculate the precision size of the symbol
            stepSize = [ i for i in asset_exchange_info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['stepSize']
            precision = int(round(-math.log(float(stepSize), 10), 0))
            # Check the amount needed in order to place a minimum order
            required_amount = float(round(float([ i for i in asset_exchange_info['filters'] if i['filterType'] == 'MIN_NOTIONAL'][0]['minNotional']), 8))
            # Get the asset names
            base_asset = asset_exchange_info['baseAsset']
            quote_asset = asset_exchange_info['quoteAsset']

            # Check for each asset selected what we have available in the wallet
            balance = pynance.wallet.balance()
            base_balance = [i for i in balance.json if i['coin'] == base_asset][0]
            base_balance_free = float(round(float(base_balance['free']), 8))
            quote_balance = [i for i in balance.json if i['coin'] == quote_asset][0]
            quote_balance_free = float(round(float(quote_balance['free']), 8))
            # Check if we are buying or if we are selling
            # One full cycle if buying asset B and selling asset B for asset A
            if order.buying:
                if base_balance_free < required_amount:
                    bot.chat(f"NOT ENOUGH {quote_asset} TO BUY {base_asset} - {base_balance_free} {quote_asset} AVAILABLE NEED MINIMUM OF {required_amount} {quote_asset}")
                else:
                    current_price = float(round(float(pynance.assets.symbols(symbol).json['price']), 8))
                    if current_price <= average:
                        quantity = float(float(float(float(quote_balance_free / current_price) / 100) * float(bot.config.wallet_amount)))
                        bot.chat(f"{base_asset} REACHED TARGET PRICE - BUYING {quantity} {base_asset}")
                        # TODO test buy order
                        # buy_order = pynance.orders.create(symbol, float(round(float(quantity - float(quantity/100)), precision)), order_id='pynanceBuyOrder')
                        buy_order = None # TODO enable
                        if buy_order is not None:
                            data = buy_order.json['fills'][0]
                            brought_price = float(round(float(data['price'] * quantity), 8))
                            order.update_data({
                                'brought_price': brought_price,
                                'quantity': quantity,
                                'buying': False
                            })
                            bot.chat(f"BROUGHT ({float(round(float(order.quantity), 8))}) {base_asset} FOR AN AMAZING ({float(round(float(sold_price), 8))}) {quote_asset}")
                        else: bot.chat(f"UNABLE TO PLACE A BUY ORDER FOR ({float(round(float(quantity), 8))}) {base_asset}")
                        print('\n\n')
                        print('-'*50)
                        print("BUYING")
                        print('-'*50)
                        print('\n\n')
                    else: bot.chat(f"CURRENT {base_asset} NOT AT BUY TARGET OF {average} - SKIPPING BUYING {base_asset}")
            else: # Trying to sell
                brought_price = order.brought_price
                minimal_profit = bot.config.profit_margin
                asset_fees = pynance.assets.fees(symbol)  # makerCommission | takerCommission
                fee_percentage = float(asset_fees.json[0]['makerCommission'])
                minimum_ask_price = float(round(brought_price + float(float(brought_price) * fee_percentage), 8))
                ask_price = float(round(float(float(minimum_ask_price) * minimal_profit), 8))
                current_price = float(round(float(pynance.assets.symbols(symbol).json['price']), 8))
                if current_price >= average:
                    bot.chat(f"{base_asset} REACHED TARGET PRICE - SELLING {order.quantity} {base_asset}")
                    # TODO test sell order
                    # sell_order = pynance.orders.create(symbol, float(round(float(quantity - float(float(quantity/100)*2.5)), precision)), buy=False, order_id='pynanceSellEntry')
                    sell_order = None
                    if sell_order is not None:
                        sold_price = float(round(float(current_price * order.quantity), 8))
                        order.update_data({
                            'active': False,
                            'sold_for': sold_price
                        })
                        bot.chat(f"SOLD ({float(round(float(order.quantity), 8))}) {base_asset} FOR AN AMAZING ({float(round(float(sold_price), 8))}) {quote_asset}")
                    else: bot.chat(f"UNABLE TO PLACE A SELL ORDER FOR ({float(round(float(order.quantity), 8))}) {base_asset}")

        return jsonify({
            'online': True,
            'execution_time': str(datetime.now()-stopwatch),
        })

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
