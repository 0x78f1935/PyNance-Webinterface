from threading import Thread
import requests
import time

class Listener(Thread):
    def __init__(self, *args, **kwargs):
        self.enbdpoint = 'http://127.0.0.1:5000/api/v1/system/'
        Thread.__init__(self, *args, **kwargs)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            data = requests.get('http://127.0.0.1:5000/api/v1/system/')
            print(data.json())
            time.sleep(1)