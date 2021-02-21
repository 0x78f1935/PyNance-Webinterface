from datetime import datetime
from backend import db


class BalanceModel(db.Model):

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
    account_type : String
        The place where the coins are held
    asset : String
        The name of the currency
    free : String
        The amount which is available to spent
    locked : String
        The amount which is available but unspendable
    """

    __tablename__ = "balance"
    id = db.Column(db.Integer, primary_key=True)
    updated = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    account_type = db.Column(db.Text, nullable=False)

    asset = db.Column(db.Text, default="Not Set")
    free = db.Column(db.Text, default="0.00000000")
    locked = db.Column(db.Text, default="0.00000000")

    def update_data(self, data: dict):
        for key, value in data.items():
            if(getattr(self, key)):
                setattr(self, key, value)
        db.session.commit()
