from datetime import datetime
from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
from uuid import uuid4


class BotModel(db.Model):
    """BotModel keeps track of the bots status"""
    __tablename__ = "Bot"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    config_id = db.Column(db.Integer, db.ForeignKey('Config.id'))
    config = db.relationship("ConfigModel", back_populates="bot")

    status_id = db.Column(db.Integer, db.ForeignKey('Status.id'))
    status = db.relationship("StatusModel", back_populates="bot")

    orders = db.relationship("OrdersModel")

    graph_type = db.Column(db.Text, default='5m')
    graph_interval = db.Column(db.Integer, default=30)
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
    
    def chat(self, message: str):
        """Updates the statusbar in the frontend

        Args:
            message (str): [The message which you would like to make appear]
        """
        self.status.message = message
        db.session.commit()

    def update_target(self, symbol: str):
        """Updates the current selected symbol in the statusbar table
        """
        self.status.target = symbol
        db.session.commit()
    
    def finished_order(self):
        """Increment the status model with +1
        """
        self.status.total_orders += 1
        db.session.commit()

    def update_average(self, average: float):
        """Keeps track of the current selected symbol average

        Args:
            average (float): [The average of the selected symbol]
        """
        self.status.average = average
        db.session.commit()
    
    def get_order(self, symbol: str):
        """Gets the order which we want to trade, if not existing we create one

        Args:
            symbol (str): [The symbol which we would like to trade]

        Returns:
            [OrderModel]: [representing order]
        """
        if self.config.sandbox: orders = [i for i in self.orders if i.symbol == symbol and i.active and i.spot == self.config.spot and i.sandbox == True]
        else: orders = [i for i in self.orders if i.symbol == symbol and i.active and i.spot == self.config.spot]
        if orders: order = orders.pop(0)
        else:
            from backend.models.orders import OrdersModel
            order = OrdersModel(
                bot_id=self.id,
                symbol=symbol,
                spot=self.config.spot,
                sandbox=self.config.sandbox
            )
            db.session.add(order)
            db.session.commit()
        return order