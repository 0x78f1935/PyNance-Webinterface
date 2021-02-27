from datetime import datetime
from backend import db

from sqlalchemy import inspect


class OrdersModel(db.Model):

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
    symbol : string, Required
        Indicates the currency for example LTCBTC
    currency_1: string, required
        Indicates the first currency of the symbol
    currency_2: string, required
        Indicates the second currency of the symbol
    quantity: string, required
        The amount we brought
    brought_price: string, required
        The price we brought the amount for
    current: boolean, optional (default True)
        When true this is the current order we are processing
    """

    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    symbol = db.Column(db.Text, nullable=False)
    currency_1 = db.Column(db.Text, nullable=False)
    currency_2 = db.Column(db.Text, nullable=False)

    quantity = db.Column(db.Text, nullable=False)
    brought_price = db.Column(db.Text, nullable=False)

    sold_for = db.Column(db.Text, default="0")
    
    fee_maker = db.Column(db.Text, nullable=False)
    fee_taker = db.Column(db.Text, nullable=False)

    current = db.Column(db.Boolean, default=True)

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