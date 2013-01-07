import time

from server.config import GARBAGE_COLLECT_INTERVAL, GARBAGE_COLLECT_MAX_AGE, KEEP_ALIVE_MAX_AGE
from server.state import GARBAGE_COLLECT, USERS
from server.util.request import get_param

def garbage_collect_users():
    """Performs garbage collection of users that haven't been seen for
    a long time.
    """
    now = time.time()
    if _needs_garbage_collect(now):
        print "user garbage collect run on users not seen since %d" % (now - GARBAGE_COLLECT_MAX_AGE)
        to_purge = []
        for userid, user in USERS['users'].iteritems():
            print 'user %s last seen %s' % (user['user'], user['last_seen'])
            if 'last_seen' in user and now - GARBAGE_COLLECT_MAX_AGE > user['last_seen']:
                print "removing user "+userid+" who hasn't been seen for a while"
                USERS['update_key'] = USERS['update_key'] + 1
                to_purge.append(userid)
        if len(to_purge) > 0:
            print 'removing %d users' % len(to_purge)
            for userid in to_purge:
                del USERS['users'][userid]
        GARBAGE_COLLECT['users'] = now

def _needs_garbage_collect(now):
    """Tells whether a garbage collect run is needed or not.
    """
    return now - GARBAGE_COLLECT['users'] > GARBAGE_COLLECT_INTERVAL

def needs_keepalive(request):
    """Tells whether user needs a keep alive query or not.
    """
    now = time.time()
    userid = get_param(request, 'id')
    if not userid:
        raise Exception("Param 'id' is required")
    if userid in USERS['users'] and 'last_seen' in USERS['users'][userid]: 
        last_seen = USERS['users'][userid]['last_seen']
        if now - KEEP_ALIVE_MAX_AGE > last_seen:
            return True
    return False
    