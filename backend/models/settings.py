from datetime import datetime
from backend import db

from sqlalchemy import inspect


class SettingsModel(db.Model):
    __tablename__ = "settings"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    valid = db.Column(db.Boolean, default=True)
    minimal_profit = db.Column(db.Float, default=20)
    wallet_amount = db.Column(db.Float, default=99)

    timeframe = db.Column(db.Text, default='1m')
    total_candles = db.Column(db.Integer, default=100)

    average_distance = db.Column(db.Float, default=0)
    selected_profit = db.Column(db.Text, default='USDT')
    
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