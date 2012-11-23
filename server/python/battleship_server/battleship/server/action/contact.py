from server.state import CONTACT_REQUESTS
from server.util import request as request_util
from server.action.base import BaseAction

STATE_WAITING = 'wait'
STATE_ACCEPTED = 'accept'
STATE_REJECTED = 'reject'

class ContactAction(BaseAction):
    """Action for contacting other users for a game."""
    
    def get_data(self):
        requesting_user, requested_user = self._read_params() 
        # test if there already is a negotiation state between those 2 users
        state = self._get_answer(requesting_user, requested_user)
        if state:
            if state != STATE_WAITING:
                # have final result, returning that
                
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
                return requesting_user
        return None
