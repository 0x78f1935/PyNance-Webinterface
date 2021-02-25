from pynance.core import Core
from pynance.wallet import Wallet
from pynance.price import Price
from pynance.orders import Orders
from datetime import datetime


class PyNance(Core):
    def __init__(self, api_key, api_secret, endpoint="https://www.binance.com", app=None):
        self.endpoint = endpoint # Needs to be before super of Core
        Core.__init__(self, api_key, api_secret, app)
        self.wallet = Wallet(self)
        self.price = Price(self)
        self.orders = Orders(self)

    def servertime(self, to_date=False, strftime=None):
        """Get the current Binance server time

        Args:
            to_date (bool, optional): Formats the date with the datetime library. Defaults to False.
            strftime (string, optional): Use strformat string format to manipulate the date. Defaults to None.

        Returns:
            str: The Binance server time formatted according to the options
        """
        response = self.get(f'{self.endpoint}/api/v3/time', signed=False)
        if to_date or strftime is not None: 
            if strftime is not None: return str(
                datetime.utcfromtimestamp(response.json['serverTime']/1000).strftime(strftime)
            )
            else: return str(datetime.utcfromtimestamp(response.json['serverTime']/1000))
        else: return str(response.json['serverTime'])

    def exchange_info(self, asset=None):
        """Get information about the exchange or about a certian asset

        Args:
            asset (string, optional): A trade currency. Defaults to None.
                                      If None returns info about the exchange and all the coins
                                      If provided it will return only info about the coin.
        """
        if asset is None: return self.get(f'{self.endpoint}/api/v3/exchangeInfo', signed=False)
        else:
            data = self.get(f'{self.endpoint}/api/v3/exchangeInfo', signed=False)
            coin = [i for i in data.json['symbols'] if i['symbol'] == asset]
            if coin: return coin.pop(0)
            else: return []