from datetime import datetime
from backend import db
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import inspect
from sqlalchemy.ext.mutable import MutableList
from sqlalchemy import PickleType
from uuid import uuid4


class StatusModel(db.Model):
    """StatusModel keeps track of the statusbar"""
    __tablename__ = "Status"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    bot = db.relationship("BotModel", back_populates="status")

    target = db.Column(db.Text, default="NO TARGET")
    message = db.Column(db.Text, default="Offline")
    total_orders = db.Column(db.Integer, default=0)
    average = db.Column(db.Float, default=0.0)

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