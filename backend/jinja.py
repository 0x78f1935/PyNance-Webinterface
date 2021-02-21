from flask import current_app
from datetime import datetime


class CustomFunctions(object):
    @staticmethod
    def project_name():
        return current_app.config['PROJECT_NAME']
