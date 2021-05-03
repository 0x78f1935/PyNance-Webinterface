from requests.exceptions import ConnectionError
from backend.models.system import SystemModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from backend.config import Config
from datetime import datetime
from flask import Flask
import requests
import time

class Listener(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)
        self.config.from_object(Config())

listener = Listener()
DEBUG = bool(listener.config['DEBUG'])
if DEBUG: endpoint = 'http://127.0.0.1:5000/api/v1/logic/'
else: endpoint = 'http://dashboard:5000/api/v1/logic/'
engine = create_engine(listener.config['SQLALCHEMY_DATABASE_URI'])
session = Session(engine)
system = session.query(SystemModel).first()
_token = system.token
session.close()
del listener

while True:
    req = requests.get(
        endpoint,
        headers={
            'token': _token
        }
    )
    j = req.json()
    print(f"{datetime.utcnow()} [{req.status_code}] -> Execution time: {j['execution_time']} | Online: {j['online']}")
    time.sleep(5)