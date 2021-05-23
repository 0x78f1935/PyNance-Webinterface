from requests.exceptions import ConnectionError
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.exc import ProgrammingError
from backend.config import Config
from datetime import datetime
from flask import Flask
import requests
import time
from json.decoder import JSONDecodeError

class Listener(Flask):
    def __init__(self):
        Flask.__init__(self, __name__)
        self.config.from_object(Config())

listener = Listener()
DEBUG = bool(listener.config['TESTING'])
if DEBUG: endpoint = 'http://127.0.0.1:5000/api/v1/logic/'
else: endpoint = 'http://pn_dashboard:5000/api/v1/logic/'
print(endpoint)
database_uri = listener.config['SQLALCHEMY_DATABASE_URI']

del listener

def get_token(database_uri):
    engine = create_engine(database_uri)
    session = Session(engine)
    from backend.models.system import SystemModel
    try: system = session.query(SystemModel).first()
    except ProgrammingError: system = None
    if system is not None: 
        token = system.token
        session.close()
        return token
    session.close()
    return None

_token = get_token(database_uri)
if _token is None or _token == '': print("Looks like first time use, waiting for setup to be completed ...")

while True:
    if _token is not None and _token != '':
        req = requests.get(
            endpoint,
            headers={
                'token': _token
            }
        )
        try:
            j = req.json()
            print(f"{datetime.utcnow()} [{req.status_code}] -> Execution time: {j['execution_time']} | Online: {j['online']}")
        except JSONDecodeError as e:
            print(e)
            print(req)
            print(req.data)
    else:
        print('Trying to obtain token')            
        _token = get_token(database_uri)

    time.sleep(5)