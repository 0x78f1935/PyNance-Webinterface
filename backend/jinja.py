from flask import current_app
from datetime import datetime

class CustomFunctions(object):
    @staticmethod
    def secret_key():
        return current_app.config['SECRET_KEY']

    @staticmethod
    def server_backend():
        return current_app.config['SERVER_BACKEND']