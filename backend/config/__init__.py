from backend.config.system import System

class Config(System):
    """
    The base of the configuration can be found in this class.
    The more complex the application, the more settings to fiddle with.

    Note
    ----
    System should super at the end of the init file
    """
    def __init__(self) -> None:
        self.DEBUG = False
        self.VERSION = "3.0.0"
        self.PROJECT_NAME = "PyNance - Webinterface"

        self.ENVIRONMENT = None
        self.SERVER_BACKEND = None
        self.LOCALE = None
        self.FALLBACK_LOCALE = None
        self.SERVER_DOCKER = None

        self.SQLALCHEMY_DATABASE_URI = None
        self.SQLALCHEMY_TRACK_MODIFICATIONS = None

        self.BINANCE_API_KEY = None
        self.BINANCE_API_SECRET = None

        # Load system configuration
        System.__init__(self)
