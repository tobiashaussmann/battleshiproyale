import time
from server.util.request import get_param
from server.state import USERS

def user_seen(request):
    """Marks a user as seen, updating her keepalive timestamp.
    """
    userid = get_param(request, 'id')
    if userid:
        user = USERS['users'].get(userid)
        if user:
            user['last_seen'] = time.time()
    