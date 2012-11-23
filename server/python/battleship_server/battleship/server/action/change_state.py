from server.state import USERS
from server.util import request as request_util
from server.action.base import BaseAction

class ChangeStateAction(BaseAction):
    """Changes the state of a user.
    """
    def get_data(self):
        userid = request_util.get_param(self.request, 'id')
        if not userid:
            raise Exception("parameter 'id' is required")
        state = request_util.get_param(self.request, 'state', '')
        user = USERS['users'].get(userid)
        if user:
            user['state'] = state
            USERS['update_key'] = USERS['update_key'] + 1
        return {'action': 'changestate', 'newstate': state }