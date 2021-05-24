from flask import Flask

from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

from backend.config import Config
from backend.views import ViewManager
from backend.jinja import CustomFunctions

from pynance import PyNance
import pathlib

db = SQLAlchemy()
cors = CORS()
migrate = Migrate()
pynance = PyNance(flask_app=True)

class Webserver(Flask):
    def __init__(self):
        public_folder = str(
            pathlib.PurePosixPath(
                pathlib.Path(__file__).resolve().parent.parent,
                'frontend',
                'dist'
            )
        )
        if not pathlib.Path(public_folder).exists(): raise Exception(
            'Frontend needs to be compiled first\n\n' \
            'cd webserver/frontend && npm run watch\n' \
            'cd webserver/frontend && npm run build'
        )

        Flask.__init__(self, __name__, 
            template_folder=public_folder,
            static_folder=public_folder,
            static_url_path=''
        )
        self.config.from_object(Config())

        if len(self.config['BINANCE_API_KEY']) <= 10: raise Exception('Binance API KEY invalid')
        if len(self.config['BINANCE_API_SECRET']) <= 10: raise Exception('Binance API SECRET invalid')

        self._setup_cors()
        self._setup_views()
        self._setup_database()
        self._setup_plugins()
        self._setup_jinja()
        self._is_populated = False

    def _setup_cors(self):
        cors.init_app(self, resources={r'/*': {'origins': ['*', 'https://developers.coinmarketcal.com/']}})

    def _setup_views(self):
        viewmanager = ViewManager(self)
        viewmanager.register()

    def _setup_database(self):
        db.init_app(self)
        migrate.init_app(self, db)

        from backend.models.keys import KeysModel
        from backend.models.system import SystemModel
        from backend.models.bot import BotModel
        from backend.models.config import ConfigModel
        from backend.models.status import StatusModel
        from backend.models.orders import OrdersModel

    def _setup_plugins(self):
        pynance.init_app(self)

    def _setup_jinja(self):
        """
        Updates jinja with custom python commands. Each new command will be callable
        in the jinja templates.
        """
        self.jinja_env.globals.update(
            secret_key=CustomFunctions.secret_key,
            server_backend=CustomFunctions.server_backend
        )

    def __call__(self, environ, start_response):
        if not self._is_populated:
            with self.app_context():
                from backend.models.system import SystemModel
                system = SystemModel.query.first()
                if system is None:
                    system = SystemModel(version=self.config['VERSION'])
                    db.session.add(system)
                    db.session.commit()

                from backend.models.config import ConfigModel
                config = ConfigModel.query.first()
                if config is None:
                    config = ConfigModel()
                    db.session.add(config)
                    db.session.commit()

                from backend.models.status import StatusModel
                status = StatusModel.query.first()
                if status is None:
                    status = StatusModel()
                    db.session.add(status)
                    db.session.commit()

                from backend.models.bot import BotModel
                bot = BotModel.query.first()
                if bot is None:
                    db.session.add(BotModel(config_id=config.id, status_id=status.id))
                    db.session.commit()
                
                if system is not None and \
                    config is not None and \
                    status is not None and \
                    bot is not None:
                    self._is_populated = True
        return super().__call__(environ, start_response)