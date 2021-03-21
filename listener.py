from requests.exceptions import ConnectionError
import requests
import time

DEBUG = False

while True:
    try:
        if DEBUG:
            data = requests.get('http://127.0.0.1:5000/api/v1/bot/')
            print(data.json())
        else:
            data = requests.get('http://dashboard:5000/api/v1/bot/')
            print(data.json())
    except ConnectionError as e: print(e)
    time.sleep(1)