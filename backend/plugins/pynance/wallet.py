class Wallet(object):
    def __init__(self, client):
        self.client = client
    
    def balance(self):
        return self.client.get(f'{self.client.endpoint}/api/v3/account', signed=True, data={})