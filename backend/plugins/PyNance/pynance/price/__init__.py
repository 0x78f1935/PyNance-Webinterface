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