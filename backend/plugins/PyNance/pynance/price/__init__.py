from pynance.core.exceptions import BinanceAPIException
from statistics import mean

class Price(object):
    def __init__(self, client):
        self.client = client
    
    def fees(self, asset=None):
        """Returns the fees in percentage of the selected asset.
        An asset can be None, if an asset is None it will return all the fees.
        
        # Maker -> Buys crypto
        # Taker -> Sells crypto

        Example
            client.price.fees() # or
            client.price.fees('LTCBTC')
        """
        if asset is not None: _filter = {"symbol": asset}
        else: _filter = {}
        return self.client.get(
            f'{self.client.endpoint}/wapi/v3/tradeFee.html',
            signed=True, 
            data=_filter
        )

    def asset(self, asset):
        """returns the price of any asset
        
        Example
            client.price.asset('LTCBTC')
        """
        return self.client.get(
            f'{self.client.endpoint}/api/v3/ticker/price',
            signed=False, 
            data={"symbol": asset}
        )
    
    def average(self, asset, timeframe=None, total_candles=60, low=True):
        """returns the price of any asset

        Parameters
            asset : str
                Represents the symbol
        
            timeframe : str
                Has to be one of the following: [1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 8H, 12H, 1D, 3D, 1W, 1M]
                Default: 1m

            total_candles: int
                The total amount of history candles to take in consideration. Max 1000
                default: 60
                When the total_candles is set to 60 and the timeframe is set to 1m you will get the average calculated
                over each minute in the last hour.
            
            low: bool
                The type of average we want to return. If low is True it takes the average of the lowest point of each candle.
                Otherwise the highest point of each candle will be used to calculate the average on
                default: True
                
        
        Example
            client.price.average('LTCBTC')
        """
        if timeframe is None: timeframe = "1m"
        if timeframe not in ["1m", "3m", "5m", "15m", "30m", "1H", "2H", "4H", "6H", "8H", "12H", "1D", "3D", "1W", "1M"]: 
            raise BinanceAPIException("Timeframe is unknown, use one of the following timeframes: [1m, 3m, 5m, 15m, 30m, 1H, 2H, 4H, 6H, 8H, 12H, 1D, 3D, 1W, 1M]")
        data = [{
            "open time": i[0],
            "open": i[1],
            "high": i[2],
            "low": i[3],
            "close": i[4],
            "volume": i[5],
            "close time": i[6],
            "quote asset volume": i[7],
            "number of trades": i[8],
            "taker buy base asset volume": i[9],
            "taker buy quote asset volume": i[10],
            "ignore.": i[11]
        } for i in self.client.get(
            f'{self.client.endpoint}/api/v3/klines',
            signed=False, 
            data={
                "symbol": asset,
                "interval": timeframe,
                "limit": total_candles
            }
        ).json]
        if low: return mean([float(i["low"]) for i in data])
        else: return mean([float(i["high"]) for i in data])