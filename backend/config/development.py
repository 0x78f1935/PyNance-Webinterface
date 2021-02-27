class Development(object):
    """
    All values in this class will overwrite the values available in __init__ and the system config.
    This provide the advantage to create a test environment but also a production environment.

    This class represents the development environment.
    """
    def __init__(self) -> None:
        super().__init__()

        self.ENVIRONMENT = "Development"

        self.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://user:admin@127.0.0.1:3306/webserver'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True

        # BINANCE  ## https://testnet.binance.vision/
        self.BINANCE_API_KEY = "oepK24J3sKucEaTHd9EuHI9FfgHp8r7jOAxwmM1rwKDsOpn5XJgHrTUqazb5isca"
        self.BINANCE_API_SECRET = "SSFSWtBcI9ew5UnOMH4I6JiCujijmEVdA8b0EIHbXTN6z5ZVvjGI7lk3fJSk8PDD"
        self.BINANCE_ENDPOINT = "https://testnet.binance.vision"