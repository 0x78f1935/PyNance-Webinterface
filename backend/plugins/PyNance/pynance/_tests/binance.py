from unittest import TestCase
from pynance import PyNance

class BinanceTest(TestCase):
    def setUp(self):
        self.pynance = PyNance(
            "oepK24J3sKucEaTHd9EuHI9FfgHp8r7jOAxwmM1rwKDsOpn5XJgHrTUqazb5isca", 
            "SSFSWtBcI9ew5UnOMH4I6JiCujijmEVdA8b0EIHbXTN6z5ZVvjGI7lk3fJSk8PDD", 
            "https://testnet.binance.vision"
        )

    
    def test_is_default_time_a_string(self):
        self.assertIsInstance(self.pynance.servertime(), str)
        
    def test_is_default_time_a_datetime_string(self):
        the_time = self.pynance.servertime(True)
        self.assertIsInstance(the_time, str)
        self.assertGreaterEqual(len(the_time), 13)
    
    def test_strftime_on_server_time(self):
        self.assertEqual(len(self.pynance.servertime(True, '%D')), 8)