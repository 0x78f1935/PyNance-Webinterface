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

        from backend.views.api.system import SystemApiView
        SystemApiView.register(self.server, route_base=f'/{self.prefix}/{self.version}/system')

        from backend.views.api.orders import OrdersApiView
        OrdersApiView.register(self.server, route_base=f'/{self.prefix}/{self.version}/orders')

        from backend.views.api.ui import UIApiView
        UIApiView.register(self.server, route_base=f'/{self.prefix}/{self.version}/ui')