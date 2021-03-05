from requests.exceptions import ConnectionError
import requests
import time

while True:
    try:
        data = requests.get('http://dashboard:5000/api/v1/system/')
        print(data.json())
    except ConnectionError as e: print(e)
    time.sleep(1)