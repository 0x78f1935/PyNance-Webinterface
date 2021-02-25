class CandleSticks(object):
    def __init__(self, client):
        self.client = client
    
    def symbol(self, name="BTC", interval="1m"):
        data = self.client.get(
            f'{self.client.endpoint}/api/v3/klines', 
            signed=False, 
            data={"symbol": name, "interval": interval}
        )
        if data is not None and data.isSucces: return [
            {
                'opentime': i[0],
                'open': i[1],
                'high': i[2],
                'low': i[3],
                'close': i[4],
                'quote_volume': i[5],
                'trades': i[6],
                'taker_buy_base': i[7],
                'taker_buy_quote': i[8],
                'ignore': i[9],
            } 
            for i in 
            data.json
        ]
        return []
