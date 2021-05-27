from backend.utils.trading import Trading
from backend import pynance
import math


class Spot(Trading):
    def __init__(self):
        Trading.__init__(self)

    @property
    def get_active_symbols(self):
        target_symbols = []
        for item in self.bot.orders:
            if item.symbol in self.bot.config.symbols and item.active and item.spot:
                target_symbols.append(item.symbol)
        return list(set([i for i in self.bot.config.symbols] + target_symbols))

    @property
    def average(self):
        """self.prepare needs to run before this method can be called

        Returns:
            Average based on configuration parameters
        """
        # Calculate the lowest average based on the total amount of candles and the timeframe
        average = pynance.assets.average(self.symbol, self.bot.config.timeframe, self.bot.config.candle_interval)
        # If supression is on, calculate the average - x% of the average
        if self.bot.config.below_average > 0:
            average = float(average - float(float(average/100) * self.bot.config.below_average))
        return average

    def prepare(self, symbol):
        self._prepare(symbol)
        # Fetch exchange information
        asset_exchange_info = pynance.assets.exchange_info(symbol).json['symbols'].pop(0)
        # Calculate the precision size of the symbol
        stepSize = [ i for i in asset_exchange_info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['stepSize']
        self.precision = int(round(-math.log(float(stepSize), 10), 0))
        if self.precision == 0: self.precision = 8
        # Check the amount needed in order to place a minimum order
        self.required_amount = float(round(float([ i for i in asset_exchange_info['filters'] if i['filterType'] == 'MIN_NOTIONAL'][0]['minNotional']), self.precision))
        # Get the asset names
        self.base_asset = asset_exchange_info['baseAsset']
        self.quote_asset = asset_exchange_info['quoteAsset']

        # Check for each asset selected what we have available in the wallet
        balance = pynance.wallet.balance()
        bb = [i for i in balance.json if i['coin'] == self.base_asset]
        bq = [i for i in balance.json if i['coin'] == self.quote_asset]
        if bb and bq:
            self.base_balance_free = float(round(float(bb[0]['free']), self.precision))
            self.quote_balance_free = float(round(float(bq[0]['free']), self.precision))
        else: 
            self.bot.chat(f"SYMBOL {symbol} SEEMS TO BE BROKEN ON BINANCE SIDE")
            return False
        return True

    def start(self):
        """self.prepare needs to run before this method can be called
        """
        if self.order.buying:
            self.bot.update_average(self.average)
            if self.quote_balance < self.required_amount: self.bot.chat(f"NOT ENOUGH {self.quote_asset} TO BUY {self.base_asset} - {self.quote_balance} {self.quote_asset} AVAILABLE NEED MINIMUM OF {self.required_amount} {self.quote_asset}")
            else:
                if self.current_price <= self.average: # HAS TO BE <= TODO change to correct comparator
                    # Calculate the quantity we can buy based on the total amount free balance available * the total % allowed for trading
                    quantity = float(float(float(float(self.quote_balance / self.current_price) / 100) * float(self.bot.config.wallet_amount)))
                    self.bot.chat(f"{self.base_asset} REACHED TARGET PRICE - BUYING {quantity} {self.base_asset}")
                    if self.bot.config.sandbox:
                        brought_price = float(round(float(self.current_price)* quantity, self.precision))
                        self.order.update_data({
                            'brought_price': brought_price,
                            'quantity': quantity,
                            'buying': False
                        })
                        self.bot.chat(f"BROUGHT IN SANBOXMODE ({float(round(float(self.order.quantity), self.precision))}) {self.base_asset} FOR AN AMAZING ({float(round(float(brought_price), self.precision))}) {self.quote_asset}")
                    else:
                        buy_order = pynance.orders.create(self.symbol, float(round(float(quantity - float(quantity/100)), self.precision)), order_id='PyNanceV3-Order-Buy')
                        if buy_order is not None:
                            data = buy_order.json['fills'][0]
                            brought_price = float(round(float(data['price'])* quantity, self.precision))
                            self.order.update_data({
                                'brought_price': brought_price,
                                'quantity': quantity,
                                'buying': False
                            })
                            self.bot.chat(f"BROUGHT ({float(round(float(self.order.quantity), self.precision))}) {self.base_asset} FOR AN AMAZING ({float(round(float(brought_price), self.precision))}) {self.quote_asset}")
                        else: self.bot.chat(f"UNABLE TO PLACE A BUY ORDER FOR ({float(round(float(quantity), self.precision))}) {self.base_asset}")
                else: self.bot.chat(f"CURRENT {self.base_asset} NOT AT BUY TARGET OF {self.average} - SKIPPING BUYING {self.base_asset}")
        else: # Trying to sell
            # This check is so if the enduser keeps trading manualy the bot keeps going. It simply
            # closes the open order where there is no quantity for and starts over with buying if possible.
            if self.base_balance < self.order.quantity and not self.bot.config.sandbox:
                self.bot.chat(f"NOT ENOUGH {self.base_asset} TO SELL - {self.base_balance} {self.base_asset} AVAILABLE NEED MINIMUM OF {self.order.quantity} {self.base_asset} DISABLING ORDER")
                self.order.update_data({'active': False, 'status': 'EXPIRED'})
            else:
                brought_price = self.order.brought_price
                minimal_profit = self.bot.config.profit_margin
                asset_fees = pynance.assets.fees(self.symbol) # makerCommission | takerCommission
                fee_percentage = float(asset_fees.json[0]['makerCommission'])
                ask_price = brought_price + float(brought_price / 100 * fee_percentage) + float(brought_price / 100 * minimal_profit)
                ask_price_a_coin = float(ask_price / self.order.quantity)
                self.bot.update_average(ask_price_a_coin)
                if self.current_price >= ask_price_a_coin:
                    self.bot.chat(f"{self.base_asset} REACHED TARGET PRICE - SELLING {self.order.quantity} {self.base_asset}")
                    if self.bot.config.sandbox:
                        sold_price = float(round(float(self.current_price) * self.order.quantity, self.precision))
                        self.order.update_data({
                            'active': False,
                            'sold_for': sold_price,
                            'status': 'PROFIT'
                        })
                        self.bot.chat(f"SOLD IN SANDBOX ({float(round(float(self.order.quantity), self.precision))}) {self.base_asset} FOR AN AMAZING ({float(round(float(sold_price), self.precision))}) {self.quote_asset}")
                    else:
                        sell_order = pynance.orders.create(self.symbol, float(round(float(self.order.quantity), self.precision)), buy=False, order_id='PyNanceV3-Order-Sell')
                        if sell_order is not None:
                            sold_price = float(round(float(self.current_price) * self.order.quantity, self.precision))
                            self.order.update_data({
                                'active': False,
                                'sold_for': sold_price,
                                'status': 'PROFIT'
                            })
                            self.bot.chat(f"SOLD ({float(round(float(self.order.quantity), self.precision))}) {self.base_asset} FOR AN AMAZING ({float(round(float(sold_price), self.precision))}) {self.quote_asset}")
                        else: self.bot.chat(f"UNABLE TO PLACE A SELL ORDER FOR ({float(round(float(self.order.quantity), self.precision))}) {self.base_asset}")
                else: self.bot.chat(f"CURRENT {self.base_asset} NOT AT SELL TARGET OF {ask_price_a_coin} - SKIPPING SELLING {self.base_asset}")
