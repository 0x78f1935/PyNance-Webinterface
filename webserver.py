from backend import Webserver
from listener import Listener

def start_le_server() -> object:
    """
    This method is used to host the backend server with gunicorn
    """
    server = Webserver()
    Listener()
    return server

server = Webserver()