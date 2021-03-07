from unittest import TestCase
from pynance import PyNance

class OrdersTest(TestCase):
    """NOTE: This endpoint is not available in the test environment.
    Therefor unable to write unittest for it unless I would provide my private token.
    """

    def setUp(self):
        self.pynance = PyNance(
            "oepK24J3sKucEaTHd9EuHI9FfgHp8r7jOAxwmM1rwKDsOpn5XJgHrTUqazb5isca", 
            "SSFSWtBcI9ew5UnOMH4I6JiCujijmEVdA8b0EIHbXTN6z5ZVvjGI7lk3fJSk8PDD", 
            "https://testnet.binance.vision"
        )

        self.data = self.pynance.orders.open('LTCBTC')
    
    def test_is_success(self):
        self.assertTrue(self.data.isSucces)
    
    def test_status_code(self):
        self.assertEqual(self.data.statuscode, 200)
    
    def test_create_order_buy_stop_limit(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        data = self.pynance.orders.create('BNBBTC', 1000, False, 5, test=True)
        self.assertEqual(data, None)

    def test_create_order_sell_stop_limit(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        data = self.pynance.orders.create('BNBBTC', 1000, True, 5, test=True)
        self.assertEqual(data, None)


    def test_create_order_buy(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        data = self.pynance.orders.create('BNBBTC', 1000.0, True, test=True)
        self.assertEqual(data.statuscode, 200)
        self.assertTrue(data.isSucces)

    def test_create_order_sell(self):
        """Doesnt work in the testenvironment therefor we test on None"""
        data = self.pynance.orders.create('BNBBTC', 1000.0, False, test=True)
        self.assertEqual(data.statuscode, 200)
        self.assertTrue(data.isSucces)
