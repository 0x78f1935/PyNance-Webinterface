from datetime import datetime
from backend import db

from sqlalchemy import inspect


class BotModel(db.Model):
    __tablename__ = "bot"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    information = db.Column(db.Text, default="Please configure me before starting")

    average_price = db.Column(db.Float, default=0)
    current_value = db.Column(db.Float, default=0)

    buying = db.Column(db.Boolean, default=True)

    def chat(self, msg):
        self.information = msg
        db.session.commit()

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