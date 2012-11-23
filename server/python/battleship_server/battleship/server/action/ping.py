from battleship.server.state import USERS
from battleship.server.util import request as request_util
from battleship.server.action.base import BaseAction

class PingAction(BaseAction):
    """Action for a pinging the system and getting the list of 
    users."""
    
    def __init__(self, request):
        BaseAction.__init__(self, request)
        
    def get_data(self):
        """Returns the user list if any change has been made since the last time
        the current user has queried the list.
        """
        user = request_util.get_param(self.request, 'user')
        data = []
        if user:
            lastupdate = USERS['users'].get(user, {}).get('updated', 0)
            self.request.user = user
            self.add_user(user)
            if lastupdate != USERS['update_key']:
                data = self.get_user_list()
                USERS['users'][self.request.user]['updated'] = USERS['update_key']
        return data 
        
    def get_user_list(self):
        """
        Returns the list of users known to the system
        """
        return {'users':USERS['users'].values()}
    
    def add_user(self, user):
        """
        Adds a known user.
        """
        if not user in USERS['users'].keys():
            USERS['update_key'] = USERS['update_key'] + 1
            USERS['users'][user] = {'name':user}