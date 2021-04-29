from datetime import datetime
from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
from uuid import uuid4


class SystemModel(db.Model):
    """System model for PyNance contains variables that will be loaded when the dashbord
    is visited for the first time. The content is created when the flask server starts.
    The content however gets only created if it doesn't exists already.
    """
    __tablename__ = "System"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = db.Column(db.Text, default="x.x.x")
    language = db.Column(db.Text, default="en")
    tos = db.Column(db.Boolean, default=False)
    authentication = db.Column(db.Boolean, default=False)
    password = db.Column(db.Text, default='')
    token = db.Column(db.Text, default='')

    def set_password(self, password):
        self.password = generate_password_hash(password)
        self.token = str(uuid4()).replace('-', '')
        db.session.commit()
    
    def check_password(self, password):
        return check_password_hash(self.password, password)

    def update_data(self, data: dict):
        """"Just throw in a json object, each key that can be mapped will be updated"

        Args:
            data (dict): The data to update with
        """
        for key, value in data.items():
            try:
                getattr(self, key)
                setattr(self, key, value)
            except AttributeError: pass
        db.session.commit()

    def to_dict(self, blacklist:list=[]):
        """Transforms a row object into a dictionary object

        Args:
            blacklist ([list]): [Columns you don't want to include in the dict]
        """
        return {c.key: getattr(self, c.key) for c in inspect(self).mapper.column_attrs if c.key not in blacklist}