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

        from backend.views.api.preference import PreferenceAPIView
        PreferenceAPIView.register(self.server, route_base=f'{self.prefix+self.version}/preference')

        from backend.views.api.system import SystemAPIView
        SystemAPIView.register(self.server, route_base=f'{self.prefix+self.version}/system')

        from backend.views.api.settings import SettingsAPIView
        SettingsAPIView.register(self.server, route_base=f'{self.prefix+self.version}/settings')

        from backend.views.api.bot import BotAPIView
        BotAPIView.register(self.server, route_base=f'{self.prefix+self.version}/bot')

        from backend.views.api.orders import OrdersAPIView
        OrdersAPIView.register(self.server, route_base=f'{self.prefix+self.version}/orders')

        from backend.views.api.backup import BackupAPIView
        BackupAPIView.register(self.server, route_base=f'{self.prefix+self.version}/backup')

        from backend.views.api.auth import AuthAPIView
        AuthAPIView.register(self.server, route_base=f'{self.prefix+self.version}/auth')