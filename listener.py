from requests.exceptions import ConnectionError
from backend.models.system import SystemModel
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
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
else: endpoint = 'http://pn_dashboard:5000/api/v1/logic/'
engine = create_engine(listener.config['SQLALCHEMY_DATABASE_URI'])
del listener

session = Session(engine)

def get_token(session):
    try: system = session.query(SystemModel).first()
    except ProgrammingError: system = None
    if system is not None: return system.token
    return None

_token = get_token(session)
if _token is None or _token == '': print("Looks like first time use, waiting for setup to be completed ...")

while True:
    if _token is not None and _token != '':
        req = requests.get(
            endpoint,
            headers={
                'token': _token
            }
        )
        j = req.json()
        print(f"{datetime.utcnow()} [{req.status_code}] -> Execution time: {j['execution_time']} | Online: {j['online']}")
    else:
        _token = get_token(session)
        if _token is not None:
            session.close()

    time.sleep(5)