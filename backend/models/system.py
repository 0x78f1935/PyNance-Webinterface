from datetime import datetime
from backend import db

from sqlalchemy import inspect


class SystemModel(db.Model):

    """
    This model keeps track of the current amount of coins available in the wallet.

    Attributes
    ----------
    __tablename__ : str
        The name of the table in the database.
    id : int
        The ID of the user. Primary Key
    updated : DateTime, Automated
        The date the user was last seen. Updates automatically.
    currency_1: string
        Indicates the first currency of the symbol
    currency_2: string
        Indicates the second currency of the symbol
    take_profit: string
        The proft taken from the trading
    online: boolean
        indicates if the bot is trading
    """

    __tablename__ = "system"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    currency_1 = db.Column(db.Text, default="BTC")
    currency_2 = db.Column(db.Text, default="USDT")

    take_profit = db.Column(db.Text, default="20")
    online = db.Column(db.Boolean, default=False, onupdate=False)

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