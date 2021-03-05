from backend.config.development import Development
from backend.config.production import Production

class System(Development, Production):
    """
    The system configuration is ment to be constant and should not be changed if not necessary.
    If you still would like to overwrite values consider using the production or development configuration file instead.
    """
    def __init__(self) -> None:
        self.MAINTAINER = "0x78f1935"
        self.GITHUB = "https://github.com/0x78f1935/PyNance-Webinterface"
        self.TWITTER = "https://twitter.com/UnicodeError"

        # When debug is False, load production environment
        if not self.DEBUG: Production.__init__(self)
        # When debug is True, load development environment
        else: Development.__init__(self)
