class Wallet(object):
    def __init__(self, client):
        self.client = client

    def balance(self, asset=None):
        data = self.client.get(f'{self.client.endpoint}/api/v3/account', signed=True, data={})
        if asset is None: return data.json['balances']
        else: 
            data = [i for i in data.json['balances'] if i['asset'] == asset]
            if data: return data.pop(0)
            else: return []
