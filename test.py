import requests
import time

while True:
    data = requests.get('http://127.0.0.1:5000/api/v1/system/')
    print(data.json())
    time.sleep(1)