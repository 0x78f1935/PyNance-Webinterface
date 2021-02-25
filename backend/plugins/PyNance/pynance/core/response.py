class Response(object):
    def __init__(self, response):
        self._succes = True if response.status_code == 200 else False
        self._ratelimited = True if response.status_code == 429 else False
        self._banned = True if response.status_code == 418 else False
        self._statuscode = response.status_code
        self._message = ''
        self._from = response.url
        self.json = response.json()

        self._set_msg(response.status_code)
        print(self._message)
    
    @property
    def isSucces(self):
        return self._succes
    
    @property
    def isRateLimited(self):
        return self._ratelimited
    
    @property
    def isBanned(self):
        return self._banned

    @property
    def statuscode(self):
        return self._statuscode
    
    @property
    def info(self):
        return self._message
    
    def _set_msg(self, statuscode):
        if statuscode == 429: 
            self._message = '[PYNANCE] You have been rate limited, stop making requests or your account might get banned'
        elif statuscode == 418: 
            self._message = '[PYNANCE] You have been temporarly banned, You made to many requests'
        elif statuscode == 200: 
            self._message = f'[PYNANCE] Request successful `{self._from}`'
