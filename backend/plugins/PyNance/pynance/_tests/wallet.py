from unittest import TestCase
from pynance import PyNance

class WalletTest(TestCase):

    def setUp(self):
        self.pynance = PyNance(
            "oepK24J3sKucEaTHd9EuHI9FfgHp8r7jOAxwmM1rwKDsOpn5XJgHrTUqazb5isca", 
            "SSFSWtBcI9ew5UnOMH4I6JiCujijmEVdA8b0EIHbXTN6z5ZVvjGI7lk3fJSk8PDD", 
            "https://testnet.binance.vision"
        )
        self.data = self.pynance.wallet.balance()

    def test_data_is_list(self):
        self.assertIsInstance(self.data, list)
    
    def test_data_has_atleast_one_value(self):
        self.assertGreater(len(self.data), 1)
    
    def test_data_first_el_is_a_dict(self):
        self.assertIsInstance(self.data[0], dict)

    def test_data_contains_btc_and_contain_all_values_needed_in_dict(self):
        btc = [i for i in self.data if i['asset'] == 'BTC'].pop(0)
        self.assertTrue(True if 'free' in btc.keys() else False)
        self.assertTrue(True if 'locked' in btc.keys() else False)
