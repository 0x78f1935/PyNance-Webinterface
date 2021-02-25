class BinanceAPIException(Exception):

    def __init__(self, msg, response):
        self.response = response
        self.msg = msg

    def __str__(self):  # pragma: no cover
        return f'[PyNance] API-Error(code={self.response.status_code}): {self.msg}\n[Pynance] Endpoint: ({self.response.url})'

class BinanceException(Exception):

    def __init__(self, msg):
        self.msg = msg

    def __str__(self):  # pragma: no cover
        return f'[PyNance] Error: {self.msg}'
