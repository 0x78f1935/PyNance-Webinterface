from pynance.core.exceptions import BinanceException
from uuid import uuid4
import pathlib

class System(object):
    """
    The system configuration is ment to be constant and should not be changed if not necessary.
    If you still would like to overwrite values consider using the production or development configuration file instead.
    """
    def __init__(self) -> None:
        self.MAINTAINER = "0x78f1935"
        self.GITHUB = "https://github.com/0x78f1935/PyNance-Webinterface"
        self.TWITTER = "https://twitter.com/UnicodeError"

        self.SECRET_KEY = str(uuid4()).replace('-', '')

        # When debug is False, load production environment
        if not self.DEBUG: filename = '.env.production'
        # When debug is True, load development environment
        else: filename = '.env.development'

        config_loc = pathlib.PurePosixPath(pathlib.Path(__file__).resolve().parent.parent.parent, filename)
        with open(config_loc, 'r') as config_file:
            data = self._clean_config_data([i for i in config_file.readlines()])

        self._load_config(data)

    def _clean_config_data(self, data):
        results = {}
        for item in data:
            if not item.startswith('//'):
                if item.endswith('\n'):
                    item = item.strip()
                attributes = item.split('=')
                key = attributes.pop(0)
                value = '='.join(attributes)
                if key != '' and value != '':
                    results[key] = value
        return results
    
    def _load_config(self, data):
        for key, value in data.items():
            if key != '' and value != '':
                try:
                    getattr(self, key)
                    setattr(self, key, value)
                except AttributeError: raise BinanceException("Invalid configuration provided")
