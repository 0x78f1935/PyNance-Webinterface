from datetime import datetime
from backend import db

from sqlalchemy import inspect


class OrderModel(db.Model):
    __tablename__ = "orders"
    id = db.Column(db.Integer, primary_key=True)
    brought = db.Column(db.DateTime, default=datetime.utcnow)
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