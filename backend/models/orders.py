from datetime import datetime
from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
from uuid import uuid4


class OrdersModel(db.Model):
    """KeysModel keeps track of API keys which can extend features within PyNance"""
    __tablename__ = "Orders"
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bot_id = db.Column(db.Integer, db.ForeignKey('Bot.id'))
    
    symbol = db.Column(db.Text, nullable=False)
    brought_price = db.Column(db.Float, default=0.0)
    quantity = db.Column(db.Float, default=0.0)
    sold_for = db.Column(db.Float, default=0.0)
    stop_loss = db.Column(db.Float, default=0.0)
    profit_target = db.Column(db.Float, default=0.0)
    buying = db.Column(db.Boolean, default=True)
    status = db.Column(db.Text, default="UNKNOWN")
    spot = db.Column(db.Boolean, default=True)
    sandbox = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    order_id = db.Column(db.BigInteger)
    client_order_id = db.Column(db.Text)

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
    
    def set_active(self, value: bool):
        self.active = value
        db.session.commit()