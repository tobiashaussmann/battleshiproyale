import time
from server.util.request import get_param
from server.util.garbagecollect import garbage_collect_users
from server.state import USERS

def user_seen(request, has_been_seen):
    """Marks a user as seen, updating her keepalive timestamp.
    """
    userid = get_param(request, 'id')
    if userid:
        user = USERS['users'].get(userid)
        if user and has_been_seen:
            user['last_seen'] = time.time()
        garbage_collect_users()
    