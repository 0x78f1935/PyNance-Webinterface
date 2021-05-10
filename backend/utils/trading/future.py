from backend.utils.trading import Trading
from backend import pynance
import math

class Futures(Trading):
    def __init__(self):
        Trading.__init__(self)

    @property
    def get_active_symbols(self):
        target_symbols = []
        for item in self.bot.orders:
            if item.symbol in self.bot.config.symbols and item.active and not item.spot:
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
        self.precision = asset_exchange_info['baseAssetPrecision']
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
        selected_leverage = self.closest(available_leverages, self.bot.config.expected_leverage)
        lev = pynance.futures.change_leverage(symbol, selected_leverage)
        if lev.info['status_code'] != 200:
            self.bot.chat(f"UNABLE TO SET {selected_leverage}X LEVERAGE FOR {symbol}")
            return False
        self.bot.chat(f"LEVERAGE HAS BEEN SET - {selected_leverage}X FOR {symbol}")

        # Set margin type
        marg = pynance.futures.change_margin_type(symbol, self.bot.config.margin_type)
        if marg.json['msg'] not in ['No need to change margin type.', 'success']:
            self.bot.chat(f"UNABLE TO SET MARGIN TYPE {self.bot.config.margin_type} FOR {symbol}")
            return False
        self.bot.chat(f"MARGIN HAS BEEN SET FOR {symbol} - {self.bot.config.margin_type} {selected_leverage}X")

        # Enable hedge mode
        pynance.futures.change_hedge_mode(True)
        return True

    def start(self):
        # Check if we have an order active
        open_orders = pynance.futures.orders.open(self.symbol)
        _ = str(float(round(self.order.quantity, self.precision_qty))).endswith('.0')
        check = str(int(round(self.order.quantity, self.precision_qty))) if _ else str(float(round(self.order.quantity, self.precision_qty)))
        if [i for i in open_orders.json if i['symbol'] == self.symbol and i['origQty'] == check]:
            self.bot.update_average(float(open_orders.json[0]['activatePrice']))
            self.bot.chat(f"FOUND OPEN ORDER FOR {self.symbol} - SKIPPING")
        # Check if we have a position open
        elif self.order.client_order_id is not None:
            order_data = pynance.futures.orders.open(self.symbol, self.order.client_order_id)
            self.bot.update_average(float(order_data.json['stopPrice']))
            if order_data.json['status'] == 'FILLED' and order_data.json['price'] == "0":
                # TODO if canceled update order_data
                if self.bot.config.allow_multiple_orders: self.engine()
                else: self.bot.chat(f'NOT ALLOWED TO PLACE MULTIPLE POSITIONS FOR {self.symbol} - SKIPPING')
            else:
                self.order.update_data({
                    'active': False,
                    'sold_for': float(order_data.json['price'])
                })
        else: self.engine()

    def engine(self):
        if self.quote_balance < self.required_amount: self.bot.chat(f"NOT ENOUGH {self.quote_asset} TO PLACE A {self.position} - {self.quote_balance} {self.quote_asset} AVAILABLE NEED MINIMUM OF {self.required_amount} {self.quote_asset}")
        else:
            if self._average_check \
                and self._volume_check:
                self.place_order()
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

    def place_order(self):
        self.bot.chat(f"OPENED A {self.position} POSITION ON {self.symbol}")
        quantity = float(round(float(float(float(self.quote_balance / self.current_price) / 100) * float(self.bot.config.wallet_amount)), self.precision_qty))
        activation_price = self.current_price - float(float(self.current_price / 100) * self.bot.config.activation_price) if self.position == 'LONG' else self.current_price + float(float(self.current_price / 100) * self.bot.config.activation_price)
        if self.bot.config.sandbox:
                brought_price = float(round(float(activation_price)* quantity, self.precision))
                self.order.update_data({
                    'brought_price': brought_price,
                    'quantity': quantity,
                    'buying': False
                })
                self.bot.chat(f"BROUGHT IN SANDBOX ({float(round(float(self.order.quantity), self.precision))}) {self.symbol} {self.position} FOR AN AMAZING ({float(round(float(brought_price), self.precision))}) {self.quote_asset}")
        else:
            order_data = {
                'symbol':self.symbol,
                'market_type':"TRAILING_STOP_MARKET",
                'side':"BUY" if self.position == 'LONG' else "SELL",
                'quantity':quantity,
                'position':self.position,
                'callbackRate':self.bot.config.in_green,
                'workingType': 'MARK_PRICE'
            }
            if self.bot.config.activation_price != 0: order_data['activationPrice'] = activation_price
            order = pynance.futures.orders.create(**order_data)
            if order.code == -4003: self.bot.chat(f"NOT ENOUGH BALANCE TO PLACE ORDER FOR {self.symbol}")
            elif 'orderId' in order.json:
                brought_price = float(round(float(activation_price)* quantity, self.precision))
                self.order.update_data({
                    'brought_price': brought_price,
                    'quantity': quantity,
                    'order_id': order.json['orderId'],
                    'client_order_id': order.json['clientOrderId'],
                    'buying': False
                })
                self.bot.chat(f"BROUGHT ({float(round(float(self.order.quantity), self.precision))}) {self.symbol} {self.position} FOR AN AMAZING ({float(round(float(brought_price), self.precision))}) {self.quote_asset}")
            else: self.bot.chat(f"UNABLE TO PLACE A {'BUY' if self.position == 'LONG' else 'SELL'}/{self.position} ORDER FOR ({float(round(float(quantity), self.precision))}) {self.base_asset}")