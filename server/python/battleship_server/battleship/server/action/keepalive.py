from server.action.base import BaseAction

class KeepAliveAction(BaseAction):
    """Action for a pinging the system and getting the list of 
    users."""
    
    def __init__(self, request):
        BaseAction.__init__(self, request)
        
    def get_data(self):
        """Returns the user list if any change has been made since the last time
        the current user has queried the list.
        """
        return {'action': 'keepalive'}
         
