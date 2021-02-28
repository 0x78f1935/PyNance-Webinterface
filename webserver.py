from backend import Webserver

def start_le_server() -> object:
    """
    This method is used to host the backend server with gunicorn
    """
    server = Webserver()
    return server

server = Webserver()