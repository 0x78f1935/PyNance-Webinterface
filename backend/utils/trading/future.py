from sqlalchemy import and_
from backend.utils.trading import Trading
from backend import pynance
import math, random

class Futures(Trading):
    def __init__(self):
        Trading.__init__(self)

    @property
    def get_active_symbols(self):
        target_symbols = []
        for item in self.bot.orders:
            if item.symbol in self.bot.config.symbols and item.active and not item.spot and item.status == "PROCESSING":
                target_symbols.append(item.symbol)
        return list(set([i for i in self.bot.config.symbols] + target_symbols))

    def closest(self, lst, value):
        """Returns the closest value from a list"""
        return lst[min(range(len(lst)), key=lambda i: abs(lst[i]-value))]

    @property
    def average(self):
        """self.prepare needs to run before this method can be called

        Returns:
            Average based on configuration parameters
        """
        # Calculate the lowest average based on the total amount of candles and the timeframe
        average = pynance.futures.assets.average(self.symbol, self.bot.config.timeframe, self.bot.config.candle_interval)
        # If supression is on, calculate the average - x% of the average
        if self.bot.config.below_average > 0:
            average = float(average - float(float(average/100) * self.bot.config.below_average))
        return average

    def prepare(self, symbol):
        self._prepare(symbol)

        # Fetch exchange information
        asset_exchange_info = pynance.futures.assets.exchange_info(symbol).json['symbols'].pop(0)
        # Calculate the precision size of the symbol
        self.precision = asset_exchange_info['pricePrecision']
        self.precision_qty = asset_exchange_info['quantityPrecision']
        # Check the amount needed in order to place a minimum order
        self.required_amount = float(round(float([ i for i in asset_exchange_info['filters'] if i['filterType'] == 'MIN_NOTIONAL'][0]['notional']), self.precision))
        # Get the asset names
        self.base_asset = asset_exchange_info['baseAsset']
        self.quote_asset = asset_exchange_info['quoteAsset']

        # Check for each asset selected what we have available in the wallet
        balance = pynance.futures.wallet.balance()
        bb = [i for i in balance.json if i['asset'] == self.base_asset]
        bq = [i for i in balance.json if i['asset'] == self.quote_asset]
        self.base_balance_free = float(round(float(bb[0]['balance']), self.precision)) if bb else 0
        self.quote_balance_free = float(round(float(bq[0]['balance']), self.precision)) if bq else 0

        # Calculate volume / Position
        volume = pynance.futures.assets.volume(symbol, period=self.bot.config.volume_timeframe, limit=self.bot.config.total_volume)
        if len(volume.json) <= 0 : 
            self.bot.chat(f'SYMBOL {symbol} SEEMS TO BE NON-EXISTING IN BINANCE-FUTURES')
            return False
        highest_long_vol = min(list(sorted(volume.json, key=lambda x: x['timestamp'])), key=lambda x:abs(x['buySellRatio']-2))
        lowest_short_vol = min(list(sorted(volume.json, key=lambda x: x['timestamp'])), key=lambda x:abs(x['buySellRatio']-0))
        average_volume_ratio = sum([volume.json[i]['buySellRatio'] for i in range(len(volume.json))]) / len(volume.json)
        self.position = 'LONG' if self.closest([0, 2], average_volume_ratio) == 2 else 'SHORT'

        # Set leverage
        leverage_bracket = pynance.futures.leverage_bracket(symbol)
        available_leverages = [ i['initialLeverage'] for i in leverage_bracket.json[0]['brackets']]
        self.selected_leverage = self.closest(available_leverages, self.bot.config.expected_leverage)
        lev = pynance.futures.change_leverage(symbol, self.selected_leverage)
        if lev.info['status_code'] != 200:
            self.bot.chat(f"UNABLE TO SET {self.selected_leverage}X LEVERAGE FOR {symbol}")
            return False
        self.bot.chat(f"LEVERAGE HAS BEEN SET - {self.selected_leverage}X FOR {symbol}")

        # Set margin type
        marg = pynance.futures.change_margin_type(symbol, self.bot.config.margin_type)
        if marg.json['msg'] not in ['No need to change margin type.', 'success']:
            self.bot.chat(f"UNABLE TO SET MARGIN TYPE {self.bot.config.margin_type} FOR {symbol}")
            return False
        self.bot.chat(f"MARGIN HAS BEEN SET FOR {symbol} - {self.bot.config.margin_type} {self.selected_leverage}X")

        # Enable hedge mode
        pynance.futures.change_hedge_mode(True)
        return True

    def start(self):
        # Check if we have an order active
        open_orders = pynance.futures.orders.open(self.symbol)
        open_order_types = [i['type'] for i in open_orders.json if i['symbol'] == self.symbol]
        availability = {
            "STOP_MARKET": False,
            "TRAILING_STOP_MARKET": False,
            "TAKE_PROFIT_MARKET": False
        }
        for order_type in open_order_types:
            if order_type == "STOP_MARKET":
                availability["STOP_MARKET"] = True
            elif order_type == "TRAILING_STOP_MARKET":
                availability["TRAILING_STOP_MARKET"] = True
            elif order_type == "TAKE_PROFIT_MARKET":
                availability["TAKE_PROFIT_MARKET"] = True
        
        can_try_2_buy = True
        position_is_open = [i for i in pynance.futures.orders.account_info().json['positions'] if i['symbol'] == self.symbol and float(i['entryPrice']) > 0]
        if availability["STOP_MARKET"] and availability["TRAILING_STOP_MARKET"] and availability["TAKE_PROFIT_MARKET"] and position_is_open:
            can_try_2_buy = False
            self.bot.chat(f"FOUND OPEN ORDER FOR {self.symbol} - SKIPPING")
        else:
            if self.bot.config.sandbox:
                if random.randint(1, 2) == 1: can_try_2_buy = False
                else: self.order.update_data({'active': False, 'status': random.choice(['PROFIT', 'PROFIT SECURED', 'LOSS'])})
            else:
                if not availability["STOP_MARKET"] and position_is_open:
                    # Fuck, algorithm broke. Try to set new STOP-LOSS.
                    can_try_2_buy = False
                    self.bot.chat(f"OPEN POSITION FOUND FOR {self.symbol} WITHOUT STOP-LOSS")
                    if not 'orderId' in self._order_stop().keys():
                        self.bot.chat(f"UNABLE TO PLACE A STOP-LOSS FOR A {self.position} POSITION WITH {self.symbol} - SKIPPING")
                elif not availability["STOP_MARKET"] and not position_is_open:
                    # We made a loss. RIP, press F for our fallen comrades, we can cancel other orders.
                    self.bot.chat(f"STOP-LOSS TRIGGERED FOR {self.position} POSITION ON {self.symbol}")
                    self._cancel_orders('LOSS')
                    availability = {"STOP_MARKET": False, "TRAILING_STOP_MARKET": False, "TAKE_PROFIT_MARKET": False}
                elif not availability["TRAILING_STOP_MARKET"]:
                    # We made profit! But not the target profit we tried to get. We locked in profit tho!
                    self.bot.chat(f"TRAILING-STOP-LOSS TRIGGERED FOR {self.position} POSITION ON {self.symbol} - PROFIT SECURED")
                    self._cancel_orders('PROFIT SECURED')
                    availability = {"STOP_MARKET": False, "TRAILING_STOP_MARKET": False, "TAKE_PROFIT_MARKET": False}
                elif not availability["TAKE_PROFIT_MARKET"]:
                    # We reached our profit goal, hooray
                    self.bot.chat(f"TAKE PROFIT TRIGGERED FOR {self.position} POSITION ON {self.symbol} - GOAL REACHED!")
                    self._cancel_orders('PROFIT')
                    availability = {"STOP_MARKET": False, "TRAILING_STOP_MARKET": False, "TAKE_PROFIT_MARKET": False}

        if self.bot.config.allow_multiple_orders: self.engine()
        elif can_try_2_buy and not availability["STOP_MARKET"] and not availability["TRAILING_STOP_MARKET"] and not availability["TAKE_PROFIT_MARKET"] and not position_is_open: self.engine()
        else: self.bot.chat(f'NOT ALLOWED TO PLACE MULTIPLE POSITIONS FOR {self.symbol} - SKIPPING')

    def engine(self):
        if self.quote_balance < self.required_amount: self.bot.chat(f"NOT ENOUGH {self.quote_asset} TO PLACE A {self.position} - {self.quote_balance} {self.quote_asset} AVAILABLE NEED MINIMUM OF {self.required_amount} {self.quote_asset}")
        else:
            if self._average_check \
                and self._volume_check:
                self.place_orders()
            else: self.bot.chat(f"SYMBOL {self.symbol} DID NOT MEET THE TRADE REQUIREMENTS - SKIPPING")
    
    @property
    def _average_check(self):
        if self.bot.config.use_average:
            self.bot.update_average(self.average)
            if self.current_price <= self.average: return True
            else: 
                self.bot.chat(f"CURRENT {self.base_asset} NOT AT BUY TARGET OF {self.average} - SKIPPING PLACING {self.position}")
                return False
        else: self.bot.update_average(self.current_price)
        return True
    
    @property
    def _volume_check(self):
        volume = pynance.futures.assets.volume(self.symbol, period=self.bot.config.volume_timeframe, limit=self.bot.config.total_volume)
        average_volume_ratio = sum([volume.json[i]['buySellRatio'] for i in range(len(volume.json))]) / len(volume.json)
        position = 'LONG' if self.closest([0, 2], average_volume_ratio) == 2 else 'SHORT'
        if self.position == position: return True
        else:
            self.bot.chat(f"UNCERTAIN ABOUT {self.position} POSITION ON {self.symbol} - SKIPPING")
        return False

    def _cancel_orders(self, status):
        """Checks if we have open orders of the current symbol, if so check if we atleast a close order.
        If not cancel all orders and prepare for a new order

        Returns:
            Boolean: True when we had to cancel orders, otherwise false
        """
        if self.order.order_id is not None and self.order.client_order_id is not None:
            pynance.futures.orders.cancel_by_order_id(self.symbol, self.order.order_id, self.order.client_order_id)
        self.order.update_data({'active': False, 'status': status})
        pynance.futures.orders.cancel_all(self.symbol)
        self.bot.chat(f'ORDERS FOR {self.symbol} HAVE BEEN STRATEGICALLY REMOVED - SKIPPING')

    def _order_market(self):
        """Places a market order. This order position will be open immidiatly
        """
        self.quantity = float(round(float(float(float(float(self.quote_balance / self.current_price) / 100) * self.bot.config.wallet_amount) * self.selected_leverage) , self.precision_qty))
        self.market_price = self.quote_balance / 100 * self.bot.config.wallet_amount
        config = {
            'symbol':self.symbol,
            'market_type':"MARKET",
            'side':"BUY" if self.position == 'LONG' else "SELL",
            'position': self.position,
            'quantity': self.quantity
        }
        open_orders = pynance.futures.orders.open(self.symbol)
        if open_orders.json and [i['type'] for i in open_orders.json if i['type'] == 'STOP_MARKET' and i['symbol'] == self.symbol]:
            data = pynance.futures.orders.create(**config)
            self.order.update_data({
                'brought_price': self.market_price,
                'quantity': self.quantity,
                'order_id': data.json['orderId'],
                'client_order_id': data.json['clientOrderId'],
                'buying': False if self.position == 'SHORT' else True
            })
            self.bot.chat(f"BROUGHT ({self.quantity}) {self.symbol} {self.position} FOR AN AMAZING ({self.market_price}) {self.quote_asset}")
            return data.json
        else:
            self.bot.chat(f"NO STOP-LOSS FOR ({self.quantity}) {self.symbol} ON {self.position} POSITION - SKIPPING")
            return {}


    def _order_stop(self):
        """Opens a closing stop order to prevent loss
        """
        self.stopPrice = float(round(float(self.current_price - float(float(self.current_price / 100) * self.bot.config.in_red)), self.precision)) \
            if self.position == 'LONG' else \
            float(round(float(self.current_price + float(float(self.current_price / 100) * self.bot.config.in_red)), self.precision))
        config = {
            'symbol':self.symbol,
            'market_type':"STOP_MARKET",
            'side':"BUY" if self.position == 'SHORT' else "SELL",
            'position':self.position,
            'stopPrice': self.stopPrice,
            'closePosition': True,
        }
        data = pynance.futures.orders.create(**config)
        self.order.update_data({'stop_loss': self.stopPrice})
        self.bot.chat(f"STOP-LOSS AT ({self.stopPrice}) FOR {self.symbol} {self.position}")
        return data.json

    def _order_trail(self):
        """Opens a trailing close order to lock in profit
        """
        config = {
            'symbol':self.symbol,
            'market_type':"TRAILING_STOP_MARKET",
            'side':"BUY" if self.position == 'SHORT' else "SELL",
            'quantity': self.quantity,
            'position':self.position,
            'callbackRate':self.bot.config.in_green,
        }
        data = pynance.futures.orders.create(**config)
        self.bot.chat(f"TRAILING-STOP-LOSS AT ({float(round(self.current_price, self.precision))}) FOR {self.symbol} {self.position}")
        return data.json

    def _order_tp(self):
        """Opens a take profit position
        """
        self.takePrice = float(round(float(self.current_price + float(float(self.current_price / 100) * self.bot.config.take_profit)), self.precision)) \
            if self.position == 'LONG' else \
            float(round(float(self.current_price - float(float(self.current_price / 100) * self.bot.config.take_profit)), self.precision))
        config = {
            'symbol':self.symbol,
            'market_type':"TAKE_PROFIT_MARKET",
            'side':"BUY" if self.position == 'SHORT' else "SELL",
            'position':self.position,
            'stopPrice':self.takePrice,
            'closePosition': True,
        }
        data = pynance.futures.orders.create(**config)
        self.order.update_data({'profit_target': self.takePrice})
        self.bot.chat(f"TAKE PROFIT SET AT ({self.takePrice}) FOR {self.symbol} {self.position}")
        return data.json

    def _order_sell(self):
        """Sells an open market order for current selected symbol.
        """
        config = {
            'symbol':self.symbol,
            'market_type':"MARKET",
            'side':"BUY" if self.position == 'SHORT' else "SELL",
            'position': "SHORT" if self.position == 'LONG' else "LONG",
            'quantity': self.quantity
        }
        data = pynance.futures.orders.create(**config)
        self.bot.chat(f'CLOSED {"SHORT" if self.position == "LONG" else "LONG"} POSITION FOR {self.symbol}')
        return data.json

    def place_orders(self):
        self.bot.chat(f"OPENING A {self.position} POSITION ON {self.symbol}")
        if self.bot.config.sandbox:
            quantity = float(round(float(float(float(float(self.quote_balance / self.current_price) / 100) * self.bot.config.wallet_amount) * self.selected_leverage) , self.precision_qty))
            brought_price = self.quote_balance / 100 * self.bot.config.wallet_amount
            stop_loss = float(round(float(self.current_price - float(float(self.current_price / 100) * self.bot.config.in_red)), self.precision)) \
                if self.position == 'LONG' else \
                float(round(float(self.current_price + float(float(self.current_price / 100) * self.bot.config.in_red)), self.precision))
            take_profit = float(round(float(self.current_price + float(float(self.current_price / 100) * self.bot.config.take_profit)), self.precision)) \
                if self.position == 'LONG' else \
                float(round(float(self.current_price - float(float(self.current_price / 100) * self.bot.config.take_profit)), self.precision))
            self.order.update_data({
                'brought_price': brought_price,
                'quantity': quantity,
                'stop_loss': stop_loss,
                'profit_target': take_profit,
                'buying': False,
                'order_id': 123456789,
                'client_order_id': 'sandbox',
            })
        else:
            if 'orderId' in self._order_stop().keys():
                if 'orderId' in self._order_market().keys():
                    self.bot.chat(f"BROUGHT ({self.quantity}) {self.symbol} {self.position} FOR AN AMAZING ({self.market_price}) {self.quote_asset}")
                    if 'orderId' in self._order_trail().keys():
                        if 'orderId' in self._order_tp().keys():
                            pass
                        else: 
                            pynance.futures.orders.cancel_all(self.symbol)
                    else: 
                        pynance.futures.orders.cancel_all(self.symbol)
                else: 
                    pynance.futures.orders.cancel_all(self.symbol)
                    self.bot.chat(f"UNABLE TO PLACE A {'BUY' if self.position == 'LONG' else 'SELL'}/{self.position} ORDER FOR ({self.quantity}) {self.base_asset} - SKIPPING")
            else:
                self.bot.chat(f"UNABLE TO PLACE A STOP-LOSS FOR A {self.position} POSITION WITH {self.symbol} - SKIPPING")
