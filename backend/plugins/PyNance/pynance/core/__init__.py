from pynance.core.exceptions import BinanceAPIException
from pynance.core.response import Response
from operator import itemgetter
import requests
import time
import hmac
import hashlib


class Core(object):
    def __init__(self, api_key, api_secret, app):
        self.api_key = api_key
        self.api_secret = api_secret

        self.session = requests.session()

        if app is not None: self.init_app(app)
        else: self._set_session_headers()

    def init_app(self, app):
        """This method can be used to instantiate a instance in a flask application.
        This flask configuration needs to contain the following variables linked to your binance
        information

        - BINANCE_API_KEY
        - BINANCE_API_SECRET
        - BINANCE_ENDPOINT
        """
        self.api_key = app.config["BINANCE_API_KEY"]
        self.api_secret = app.config["BINANCE_API_SECRET"]
        self.endpoint = app.config['BINANCE_ENDPOINT']
        self._set_session_headers()
    
    def _set_session_headers(self):
        """Sets the headers to make requests with the binance API based on the provided token information"""
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'binance/PyNance',
            'X-MBX-APIKEY': self.api_key
        })
    
    def _request(self, method, endpoint, signed=True, force_params=True, **kwargs):
        """This method is a generic method to handle all the requests with.

        Args:
            method (string): GET,POST,PUT,ETC,ETC,..
            endpoint (string): The endpoint you would like to call
            signed (bool, optional): When enabled sign the request with authentication info. Defaults to True.
            force_params (bool, optional): When true the data will be formatted in the url instead. Defaults to True.
        """
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

        if 'x-mbx-used-weight' in self.response.headers.keys(): 
            print(f'[PYNANCE] Weight: {self.response.headers["x-mbx-used-weight"]} kg')

        return self._handle_response()

    def _sign(self, data:dict):
        """Signs the request with the authentication information provided by the enduser."""
        ordered_data = self._order(data)
        query_string = '&'.join(["{}={}".format(d[0], d[1]) for d in ordered_data])
        m = hmac.new(self.api_secret.encode('utf-8'), query_string.encode('utf-8'), hashlib.sha256)
        return m.hexdigest()

    def _order(self, data:dict):
        """Orders the data so Binance accepts the request"""
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
    
    def _handle_response(self):
        """Checks what status code we retrieved from the response of our request and act accordingly to it"""
        if self.response.status_code == 429:
            print(self.response.json())  # I would like to know what the payload looks like
            BinanceAPIException(
                'You have been rate limited, stop making requests or your account might get banned', 
                self.response
            )
        elif self.response.status_code == 418:
            print(self.response.json()) # I would like to know what the payload looks like
            BinanceAPIException(
                'You have been temporarly banned, You made to many requests', 
                self.response
            )
        elif self.response.status_code == 200:
            return self._objectify()
        elif self.response.status_code == 404:
            BinanceAPIException('Page not found', self.response)
        else:
            print(self.response.json()) # I would like to know what the payload looks like
            BinanceAPIException('Unknown error', self.response)
    
    def _objectify(self):
        if self.response: return Response(self.response)
        return None

    def get(self, endpoint, signed=False, **kwargs):
        """Executes a get request with the generic self._request method.

        Args:
            endpoint (string): The endpoint to talk to
            signed (bool, optional): Signs the request with the authentication information provided. Defaults to False.

        Example:
            client.get(
                f'{client.endpoint}/api/v3/klines', 
                signed=False, 
                data={"symbol": "LTCBTC", "interval": "1m"}
            )
        """
        return self._request('get', endpoint, signed, **kwargs)
    
    def post(self, endpoint, signed=False, **kwargs):
        """Executes a post request with the generic self._request method.

        Args:
            endpoint (string): The endpoint to talk to
            signed (bool, optional): Signs the request with the authentication information provided. Defaults to False.

        Example:
            client.post(
                f'{client.endpoint}/api/v3/order', 
                signed=False, 
                data={"symbol": "LTC", "quantity": "1"}
            )
        """
        return self._request('post', endpoint, signed, **kwargs)

    def delete(self, endpoint, signed=False, **kwargs):
        """Executes a delete request with the generic self._request method.

        Args:
            endpoint (string): The endpoint to talk to
            signed (bool, optional): Signs the request with the authentication information provided. Defaults to False.

        Example:
            client.delete(
                f'{client.endpoint}/api/v3/order', 
                signed=False, 
                data={"symbol": "LTC", "origClientOrderId": "1"}
            )
        """
        return self._request('delete', endpoint, signed, **kwargs)