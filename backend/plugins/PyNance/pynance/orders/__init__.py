from pynance.core.exceptions import BinanceException
from uuid import uuid4

class Orders(object):
    def __init__(self, client):
        self.client = client
    
    def open(self, asset=None):
        """Retrieves a collection of all open orders

        Example
            client.orders.open() # or
            client.orders.open('LTCBTC')
        """
        if asset is None: _filter = {}
        else: _filter = {'symbol': asset}
        return self.client.get(f'{self.client.endpoint}/api/v3/openOrders', signed=True, data=_filter)

    def create(self, asset=None, quantity=None, buy=True, stop_price=None, test=False, order_id=str(uuid4())):
        """This method is able to create different kind of buy/sell order on market value.
        Stop limit / take profit is supported if the stop_price is provided.
        Based on the buy boolean the stop_price will be set accordingly.
        
        Args:
            asset (string): The coin which we are currently trading
            quantity (float): The total amount you would like to trade.
            buy (bool, optional): When False the order will be a sell order. Defaults to True.
            stop_price (float, optional): When provided a stop/take profit will be set.
                                          When buy is True take profit will be set
                                          when buy is False stop loss will be set
                                          Defaults to None.
            test (bool, optional): When True the order will be created in the test environment. 
                                   Defaults to False.
            order_id (string, optional): Reference to the order created. Wil be randomly generated with a uuid4 if not set

        Raises:
            BinanceException: Happens when asset or quantity is not provided
        
        Example
            client.orders.create('BTCUSDT', '1000', False, 5.22, test=True)

        NOTE: The error `{'code': -1013, 'msg': 'Filter failure: LOT_SIZE'}` indicates that the precision of the quantity is incorrect.
        """
        if asset is None or quantity is None: raise BinanceException("Asset and quantity are required")
        _filter = {"symbol":asset, "quantity": quantity}
        if buy: side = "BUY"
        else: side = "SELL"
        _filter['side'] = side
        if stop_price is None: _filter['type'] = "MARKET"
        else:
           if buy: buy_type = "TAKE_PROFIT" 
           else: buy_type = "STOP_LOSS"
           _filter['type'] = buy_type
           _filter['stopPrice'] = stop_price
        
        if test: endpoint = f'{self.client.endpoint}/api/v3/order/test'
        else: endpoint = f'{self.client.endpoint}/api/v3/order'
        return self.client.post(endpoint, signed=True, data=_filter)

    def cancel(self, asset=None, order_id=None, test=True):
        """Cancel an order based on the asset and order ID

        Args:
            asset (string): The coin which we are currently canceling from trade
            order_id (string, optional): the unique indentifier of an already placed order.
                                         If not provided this method will cancel all orders related to the asset

        Raises:
            BinanceException: Happens when asset or order_id is not set.
        """
        if asset is None: raise BinanceException("Asset and quantity are required")
        if order_id is None: 
            endpoint = f'{self.client.endpoint}/api/v3/openOrders'
            _filter = {"symbol": asset}
        else: 
            endpoint = f'{self.client.endpoint}/api/v3/order'
            _filter = {"symbol": asset, "origClientOrderId": order_id}
        if test: endpoint += '/test'
        return self.client.delete(endpoint, signed=True, data=_filter)