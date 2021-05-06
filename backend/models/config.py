from datetime import datetime
from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from uuid import uuid4


class ConfigModel(db.Model):
    """ConfigModel keeps track of the trade configuration set in /trades"""
    __tablename__ = "Config"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bot = db.relationship("BotModel", back_populates="config")

    symbols = db.Column(MutableList.as_mutable(PickleType), default=[])
    timeframe = db.Column(db.Text, default="1h")
    candle_interval = db.Column(db.Integer, default=100)
    wallet_amount = db.Column(db.Float, default=100)
    below_average = db.Column(db.Float, default=5)
    profit_margin = db.Column(db.Float, default=35)
    profit_as = db.Column(db.Text, default="USDT")
    spot = db.Column(db.Boolean, default=True)
    sandbox = db.Column(db.Boolean, default=True)

    # Futures
    expected_leverage = db.Column(db.Float, default=5)
    volume_timeframe = db.Column(db.Text, default="5m")
    total_volume = db.Column(db.Integer, default=30)
    margin_type = db.Column(db.Text, default="ISOLATED")
    default_stop_loss = db.Column(db.Float, default=0.02)
    in_green = db.Column(db.Float, default=2)
    move_stop_loss = db.Column(db.Float, default=1)
    total_tp = db.Column(db.Float, default=5)
    take_profit = db.Column(db.Float, default=5)
    use_average = db.Column(db.Boolean, default=False)
    
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
    
    def remove_sandbox(self):
        from backend.models.orders import OrdersModel
        sandbox_items = OrdersModel.query.filter(OrdersModel.sandbox == True).delete()
        db.session.commit()