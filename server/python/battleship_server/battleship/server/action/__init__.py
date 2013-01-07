from server.util import request as request_util
from server.util import garbagecollect as garbagecollect_util
from server.action.ping import PingAction
from server.action.contact import ContactAction
from server.action.change_state import ChangeStateAction
from server.action.confirm_contact import ConfirmContactAction
from server.action.keepalive import KeepAliveAction

def get_action(request):
    """Returns an action that was required by the request.
    """
    if request.path == '/ping' and garbagecollect_util.needs_keepalive(request):
        return KeepAliveAction(request)
    elif request.path == '/ping':
        return PingAction(request)
    elif request.path == '/contact':
        return ContactAction(request)
    elif request.path == '/change_state':
        return ChangeStateAction(request)
    elif request.path == '/confirm_contact':
        return ConfirmContactAction(request)
    else:
        raise Exception("Unknown Action")
