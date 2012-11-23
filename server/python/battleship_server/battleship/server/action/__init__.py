from battleship.server.util import request as request_util
from battleship.server.action.ping import PingAction

def get_action(request):
    """Returns an action that was required by the request.
    """
    if request.path == '/ping':
        return PingAction(request)
    else:
        raise Exception("Unknown Action")
