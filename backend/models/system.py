from datetime import datetime
from backend import db

from sqlalchemy import inspect


class SystemModel(db.Model):
    __tablename__ = "system"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    online = db.Column(db.Boolean, default=False, onupdate=False)

    tos_agreement = db.Column(db.Boolean, default=False)

    currency_1 = db.Column(db.Text, default="BTC")
    currency_2 = db.Column(db.Text, default="USDT")

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