from unittest import TestSuite as BaseSuite
from unittest import TextTestRunner

from pynance._tests.wallet import WalletTest
from pynance._tests.price import PriceTest
from pynance._tests.orders import OrdersTest
from pynance._tests.binance import BinanceTest


class TestSuite(BaseSuite):
    def __init__(self):
        BaseSuite.__init__(self)
        self._test_cases = {
            'test_orders': OrdersTest,
            'test_price': PriceTest,
            'test_wallet': WalletTest,
            'test_client': BinanceTest,
        }
        self._instantate()
    
    def _instantate(self):
        for key, value in self._test_cases.items():
            self.addTest(value(key))

if __name__ == '__main__':
    runner = TextTestRunner()
    runner.run(TestSuite())