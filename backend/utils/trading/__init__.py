from backend import pynance
from datetime import datetime


class Trading(object):
    def __init__(self):
        self.stopwatch = datetime.now()

        from backend.models.bot import BotModel
        self.bot = BotModel.query.first()
        self.order = None
        self.precision = 0
        self.required_amount = 0
        self.symbol = ''
        self.base_asset = ''
        self.quote_asset = ''
        self.base_balance_free = 0
        self.quote_balance_free = 0
        self.position = ''

    def fetch_results(self):
        return {
            'online': self.bot.online,
            'execution_time': str(datetime.now()-self.stopwatch),
        }

    @property
    def can_trade(self):
        if not self.bot.online:
            self.bot.chat("CURRENTLY OFFLINE")
            return False
        
        binance_status = pynance.system.maintenance()
        if binance_status.json['status'] != 0:
            self.bot.chat("BINANCE IS CURRENTLY UNAVAILABLE")
            return False
        
        if len(self.bot.config.symbols) <= 0:
            self.bot.chat("NO SYMBOL CONFIGURED TO TRADE WITH")
            return False
        return True
    
    def _prepare(self, symbol):
        self.symbol = symbol
        self.bot.update_target(symbol)
        self.bot.chat(f"CURRENT SYMBOL SELECTED - {symbol}")
        
        # Creates an order in the database if this is not an existing order, otherwise returns the existing order
        self.order = self.bot.get_order(symbol)

    @property
    def base_balance(self):
        """self.prepare needs to run before this method can be called
        """
        return self.base_balance_free

    @property
    def quote_balance(self):
        """self.prepare needs to run before this method can be called
        """
        return self.quote_balance_free

    @property
    def current_price(self):
        """self.prepare needs to run before this method can be called
        """
        if self.order.spot: return float(round(float(pynance.assets.symbols(self.symbol).json['price']), self.precision))
        else: return float(round(float(pynance.futures.assets.symbols(self.symbol).json['price']), self.precision))

from backend.utils.trading.spot import Spot
from backend.utils.trading.future import Futures