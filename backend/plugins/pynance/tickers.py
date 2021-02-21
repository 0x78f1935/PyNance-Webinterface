class Tickers(object):
    def __init__(self, client):
        self.client = client
    
    def book_ticker(self):
        return self.client.get(f'{self.client.endpoint}/api/v3/ticker/bookTicker', signed=False, data={})