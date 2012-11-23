from server.state import CONTACT_REQUESTS, GAMES, USERS
from server.util import request as request_util
from server.action.base import BaseAction

STATE_WAITING = 'wait'
STATE_ANSWERING = 'answering'
STATE_ACCEPTED = 'accept'
STATE_REJECTED = 'reject'

class ContactAction(BaseAction):
    """Action for contacting other users for a game."""
    
    def get_data(self):
        requesting_user, requested_user = self._read_params() 
        # test if there already is a negotiation state between those 2 users
        state = self._get_answer(requesting_user, requested_user)
        if state:
            if state != STATE_WAITING and state != STATE_ANSWERING:
                # have final result, returning that
                if state == STATE_ACCEPTED:
                    self._start_game(requesting_user, requested_user)
                else:
                    self._cancel_game(requesting_user, requested_user)
                return {'action': 'contact', 'id': requesting_user, 'other': requested_user, 'result': state}
        else:
            CONTACT_REQUESTS[requesting_user] = {'requested_user': requested_user, 'state': STATE_WAITING}
        return []
        
    def _read_params(self):
        requesting_user = request_util.get_param(self.request, 'id')
        requested_user = request_util.get_param(self.request, 'other')
        if not requesting_user:
            raise Exception("Param 'id' is required")
        if not requested_user:
            raise Exception("Param 'other' is required")
        return requesting_user, requested_user
    
    def _cancel_game(self, requesting_user, requested_user):
        """Cancels the game proposal between the users.
        """
        del CONTACT_REQUESTS[requesting_user]
        
        user1 = USERS['users'].get(requesting_user)
        user2 = USERS['users'].get(requested_user)
        if user1 and user2:
            user1['state'] = 'online'
            user2['state'] = 'online'
        USERS['update_key'] = USERS['update_key'] + 1
    
    def _start_game(self, requesting_user, requested_user):
        """Starts a game between the user and removes the contact request.
        """
        del CONTACT_REQUESTS[requesting_user]
        GAMES[requesting_user] = requested_user
        
        user1 = USERS['users'].get(requesting_user)
        user2 = USERS['users'].get(requested_user)
        if user1 and user2:
            user1['state'] = 'ingame'
            user2['state'] = 'ingame'
        USERS['update_key'] = USERS['update_key'] + 1
        
    def _get_answer(self, requesting_user, requested_user):
        """Returns an answer to the contact request.
        """
        if requesting_user in CONTACT_REQUESTS.keys():
            if CONTACT_REQUESTS.get(requesting_user, {}).get('requested_user', '') == requested_user:
                return CONTACT_REQUESTS[requesting_user]['state']
            
    def get_contact_request_for(self, user):
        """Tells whether a contact request exists for the current user.
        """
        for requesting_user, requested_user in CONTACT_REQUESTS.iteritems():
            if requested_user.get('requested_user', '') == user:
                if CONTACT_REQUESTS[requesting_user]['state'] == STATE_WAITING:
                    CONTACT_REQUESTS[requesting_user]['state'] = STATE_ANSWERING
                    return requesting_user
        return None
