from backend import pynance
from datetime import datetime
import math


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
    
    def prepare(self, symbol):
        self.symbol = symbol
        self.bot.update_target(symbol)
        self.bot.chat(f"CURRENT SYMBOL SELECTED - {symbol}")
        
        # Creates an order in the database if this is not an existing order, otherwise returns the existing order
        self.order = self.bot.get_order(symbol)

        # Fetch exchange information
        asset_exchange_info = pynance.assets.exchange_info(symbol).json['symbols'].pop(0)
        # Calculate the precision size of the symbol
        stepSize = [ i for i in asset_exchange_info['filters'] if i['filterType'] == 'LOT_SIZE'][0]['stepSize']
        self.precision = int(round(-math.log(float(stepSize), 10), 0))
        # Check the amount needed in order to place a minimum order
        self.required_amount = float(round(float([ i for i in asset_exchange_info['filters'] if i['filterType'] == 'MIN_NOTIONAL'][0]['minNotional']), 8))
        # Get the asset names
        self.base_asset = asset_exchange_info['baseAsset']
        self.quote_asset = asset_exchange_info['quoteAsset']

        # Check for each asset selected what we have available in the wallet
        balance = pynance.wallet.balance()
        bb = [i for i in balance.json if i['coin'] == self.base_asset]
        bq = [i for i in balance.json if i['coin'] == self.quote_asset]
        if bb and bq:
            self.base_balance_free = float(round(float(bb[0]['free']), 8))
            self.quote_balance_free = float(round(float(bq[0]['free']), 8))
        else: self.bot.chat(f"SYMBOL {symbol} SEEMS TO BE BROKEN ON BINANCE SIDE")

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
        return float(round(float(pynance.assets.symbols(self.symbol).json['price']), self.precision))

from backend.utils.trading.spot import Spot
from backend.utils.trading.future import Futures