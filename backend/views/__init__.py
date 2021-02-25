class ViewManager(object):
    """
    This class is a representation of any router 'class'.
    It just registers all views listed in the self.register method.
    """
    def __init__(self, server) -> None:
        super().__init__()
        self.server = server
        self.prefix = "/api"
        self.version = "/v1"
    
    def register(self) -> None:
        """
        This method register the views to the server object.
        """
        from backend.views.homepage import HomePageView
        HomePageView.register(self.server, route_base='/')

        from backend.views.ping import PingPageView
        PingPageView.register(self.server, route_base=f'/{self.prefix}/{self.version}/ping')

        from backend.views.test import TestPageView
        TestPageView.register(self.server, route_base=f'/test')

        from backend.views.crontabs.balance import BalanceCrontabView
        BalanceCrontabView.register(self.server, route_base=f'/{self.prefix}/{self.version}/crontab/balance')

        from backend.views.api.symbols import SymbolsApiView
        SymbolsApiView.register(self.server, route_base=f'/{self.prefix}/{self.version}/symbols')

        from backend.views.api.candlesticks import CandleSticksApiView
        CandleSticksApiView.register(self.server, route_base=f'/{self.prefix}/{self.version}/candlesticks')

        from backend.views.api.balance import BalanceApiView
        BalanceApiView.register(self.server, route_base=f'/{self.prefix}/{self.version}/balance')