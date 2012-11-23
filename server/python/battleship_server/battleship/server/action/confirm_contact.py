from server.state import USERS, CONTACT_REQUESTS
from server.util import request as request_util
from server.action.base import BaseAction

class ConfirmContactAction(BaseAction):
    """Confirms or rejects a pairing.
    """
    def get_data(self):
        requesting_user, requested_user, result = self._read_params()
        self._set_answer(requesting_user, requested_user, result)
        return {'action': 'confirm_contact', 'newstate': result }
    
    def _set_answer(self, requesting_user, requested_user, result):
        """Answers to the contact request.
        """
        if requesting_user in CONTACT_REQUESTS.keys():
            if CONTACT_REQUESTS.get(requesting_user, {}).get('requested_user', '') == requested_user:
                CONTACT_REQUESTS[requesting_user]['state'] = result
    
    def _read_params(self):
        requested_user = request_util.get_param(self.request, 'id')
        requesting_user = request_util.get_param(self.request, 'other')
        result = request_util.get_param(self.request, 'result')
        if not requested_user:
            raise Exception("Param 'id' is required")
        if not requesting_user:
            raise Exception("Param 'other' is required")
        if not result:
            raise Exception("Param 'result' is required")
        return requesting_user, requested_user, result