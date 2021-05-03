from backend import Webserver, db
from sqlalchemy.sql import text
from backend.cli import register

def create_server() -> object:
    """
    This method is used to host the backend server with gunicorn
    """
    server = Webserver()
    from backend import db
    with server.app_context():
        try:
            db.session.query('1').from_statement(text('SELECT 1')).all()
            can_connect = True
        except Exception as e:
            exit(1)
    # Listener()
    register(server)
    return server

server = Webserver()
_database = db # In use by the listener
register(server)