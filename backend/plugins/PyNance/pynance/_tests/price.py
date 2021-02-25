from unittest import TestCase
from pynance import PyNance

class PriceTest(TestCase):
    """NOTE: This endpoint is not available in the test environment.
    Therefor unable to write unittest for it unless I would provide my private token.
    """

    def setUp(self):
        self.pynance = PyNance(
            "oepK24J3sKucEaTHd9EuHI9FfgHp8r7jOAxwmM1rwKDsOpn5XJgHrTUqazb5isca", 
            "SSFSWtBcI9ew5UnOMH4I6JiCujijmEVdA8b0EIHbXTN6z5ZVvjGI7lk3fJSk8PDD", 
            "https://testnet.binance.vision"
        )
    
        self.data = self.pynance.price.asset('LTCBTC')
    
    def test_is_success(self):
        self.assertTrue(self.data.isSucces)
    
    def test_status_code(self):
        self.assertEqual(self.data.statuscode, 200)
    
    def test_json(self):
        self.assertIn('symbol', self.data.json.keys())
        self.assertIn('price', self.data.json.keys())