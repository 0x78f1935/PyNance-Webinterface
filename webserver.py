from backend import Webserver
from sqlalchemy.sql import text
# from listener import Listener

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
    return server

server = Webserver()