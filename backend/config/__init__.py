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
        self.DEBUG = True
        self.VERSION = "1.0.0"
        self.PROJECT_NAME = "PyNance - Webinterface"

        # Load system configuration
        System.__init__(self)
