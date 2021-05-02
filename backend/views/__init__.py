from flask import redirect, url_for, request, current_app

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

        @server.errorhandler(404)
        def catch_all(path):
            """
            Redirects each non existing endpoint to the main page.
            When `API` is included in the url we ignore this redirect.
            """
            if 'api' not in request.base_url:
                return redirect(url_for('HomePageView:get')) 
    
    def register(self) -> None:
        """
        This method register the views to the server object.
        """
        from backend.views.homepage import HomePageView
        HomePageView.register(self.server, route_base='/')

        from backend.views.api.system import SystemApiView
        SystemApiView.register(self.server, route_base=f'{self.prefix+self.version}/system')

        from backend.views.api.keys import KeysApiView
        KeysApiView.register(self.server, route_base=f'{self.prefix+self.version}/keys')

        from backend.views.api.coinmarketcal import CoinMarketApiView
        CoinMarketApiView.register(self.server, route_base=f'{self.prefix+self.version}/coinmarketcal')

        from backend.views.api.wallet import WalletApiView
        WalletApiView.register(self.server, route_base=f'{self.prefix+self.version}/wallet')

        from backend.views.api.trades import TradesApiView
        TradesApiView.register(self.server, route_base=f'{self.prefix+self.version}/trades')

        from backend.views.api.klines import KlinesApiView
        KlinesApiView.register(self.server, route_base=f'{self.prefix+self.version}/klines')
