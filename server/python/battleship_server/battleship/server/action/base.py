"""Base class for actions.
"""
class BaseAction(object):
    
    def __init__(self, request):
        self.request = request
        
    def get_data(self):
        return None