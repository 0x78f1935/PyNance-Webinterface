from backend.plugins.pynance.exceptions import BinanceAPIException
from backend.plugins.pynance.response import Response
from operator import itemgetter
import requests
import time
import hmac
import hashlib


class PyNane(object):
    def __init__(self, app=None):
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        self.endpoint = app.config['BINANCE_ENDPOINT']
        self.api_secret = app.config["API_SECRET"]

        self.session = requests.session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'binance/PyNance',
            'X-MBX-APIKEY': app.config["API_KEY"]
        })
    
    def objectify(self):
        if self.response: return Response(self.response)
        return None

    def handle_response(self):
        if self.response.status_code == 429:
            print(self.response.json())
            BinanceAPIException(
                'You have been rate limited, stop making requests or your account might get banned', 
                self.response
            )
        elif self.response.status_code == 418:
            print(self.response.json())
            BinanceAPIException(
                'You have been temporarly banned, You made to many requests', 
                self.response
            )
        elif self.response.status_code == 200:
            return self.objectify()
        else:
            print(self.response.json())
            BinanceAPIException('Unknown error', self.response)

    def _order(self, data):
        has_signature = False
        params = []
        for key, value in data.items():
            if key == 'signature':
                has_signature = True
            else:
                params.append((key, value))
        # sort parameters by key
        params.sort(key=itemgetter(0))
        if has_signature:
            params.append(('signature', data['signature']))
        return params

    def _sign(self, data):
        ordered_data = self._order(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    def _request(self, method, endpoint, signed=True, force_params=True, **kwargs):
        # Set timeout for the request
        kwargs['timeout'] = 10

        data = kwargs.get('data', None)
        # Check if the request contains data
        if data and isinstance(data, dict):
            kwargs['data'] = data

            # find any requests params passed and apply them
            if 'requests_params' in kwargs['data']:
                # merge requests params into kwargs
                kwargs.update(kwargs['data']['requests_params'])
                del(kwargs['data']['requests_params'])

        if signed: # generate signature
            kwargs['data']['timestamp'] = int(time.time() * 1000)
            kwargs['data']['signature'] = self._sign(kwargs['data'])
        
        # sort get and post params to match signature order
        if data:
            # sort post params
            kwargs['data'] = self._order(kwargs['data'])
            # Remove any arguments with values of None.
            null_args = [i for i, (key, value) in enumerate(kwargs['data']) if value is None]
            for i in reversed(null_args):
                del kwargs['data'][i]

        # if get request assign data array to params value for requests lib
        if data and (method == 'get' or force_params):
            kwargs['params'] = '&'.join('%s=%s' % (data[0], data[1]) for data in kwargs['data'])
            del(kwargs['data'])

        self.response = getattr(self.session, method)(endpoint, **kwargs)
        print(self.response.url)
        return self.handle_response()
    
    def get(self, endpoint, signed=False, **kwargs):
        return self._request('get', endpoint, signed, **kwargs)

    def post(self, endpoint, signed=False, **kwargs):
        return self._request('post', endpoint, signed, **kwargs)