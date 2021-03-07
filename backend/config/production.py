class Production(object):
    """
    All values in this class will overwrite the values available in __init__ and the system config.
    This provide the advantage to create a test environment but also a production environment.

    This class represents the production environment.
    """
    def __init__(self) -> None:
        super().__init__()

        self.ENVIRONMENT = "Production"

        self.SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Y0uShoulDchAngETHIS!1!!1!@database:3306/PYNANCE'
        self.SQLALCHEMY_TRACK_MODIFICATIONS = True

        # BINANCE
        self.BINANCE_API_KEY = ""
        self.BINANCE_API_SECRET = ""
        self.BINANCE_ENDPOINT = "https://www.binance.com"