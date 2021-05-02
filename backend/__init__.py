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

        self._setup_cors()
        self._setup_views()
        self._setup_database()
        self._setup_plugins()
        self._setup_jinja()

    def _setup_cors(self):
        cors.init_app(self, resources={r'/*': {'origins': ['*', 'https://developers.coinmarketcal.com/']}})

    def _setup_views(self):
        ViewManager(self).register()

    def _setup_database(self):
        db.init_app(self)
        migrate.init_app(self, db)

        from backend.models.keys import KeysModel
        from backend.models.system import SystemModel
        from backend.models.bot import BotModel
        from backend.models.config import ConfigModel
        from backend.models.status import StatusModel
        from backend.models.orders import OrdersModel

        with self.app_context():
            try:
                self._setup_first_time_database_system_configuration()
            except Exception as e: print(e)

    def _setup_first_time_database_system_configuration(self):
        from backend.models.system import SystemModel
        model = SystemModel.query.first()
        if model is None: db.session.add(SystemModel(version=self.config['VERSION']))
       
        db.session.commit()
        pass

    def _setup_plugins(self):
        pynance.init_app(self)

    def _setup_jinja(self):
        """
        Updates jinja with custom python commands. Each new command will be callable
        in the jinja templates.
        """
        self.jinja_env.globals.update(
            secret_key=CustomFunctions.secret_key,
        )