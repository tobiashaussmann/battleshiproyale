from datetime import datetime
from server.state import USERS
from server.util import request as request_util
from server.action.base import BaseAction
from server.action.contact import ContactAction

class PingAction(BaseAction):
    """Action for a pinging the system and getting the list of 
    users."""
    
    def __init__(self, request):
        BaseAction.__init__(self, request)
        
    def get_data(self):
        """Returns the user list if any change has been made since the last time
        the current user has queried the list.
        """
        userid = request_util.get_param(self.request, 'id')
        if not userid:
            raise Exception("Param 'id' is required")
        
        username = request_util.get_param(self.request, 'user')
        highscore = request_util.get_param(self.request, 'highscore', 0)
        
        init = request_util.get_param(self.request, 'init', 'false')
        data = []
        lastupdate = USERS['users'].get(userid, {}).get('updated', 0)
        self.request.user = userid
        self.add_user(userid, username, highscore)
        if lastupdate != USERS['update_key'] or init == 'true':
            data = self.get_user_list()
            USERS['users'][self.request.user]['updated'] = USERS['update_key']
            data['action'] = 'ping'
            if init == 'true':
                USERS['users'][self.request.user]['state'] = ''
        
        # test contact action if any
        contact_action = ContactAction(self.request)
        contact_request = contact_action.get_contact_request_for(userid)
        if contact_request:
            return {'action': 'contact_request', 'other': contact_request}
         
        return data 
    
        
    def get_user_list(self):
        """
        Returns the list of users known to the system
        """
        return {'users':USERS['users'].values()}
    
    def add_user(self, userid, username, highscore):
        """
        Adds a known user.
        """
        if not userid in USERS['users'].keys():
            USERS['update_key'] = USERS['update_key'] + 1
            USERS['users'][userid] = {'id':userid, 'user': username, 'highscore': highscore, 'state': ''}