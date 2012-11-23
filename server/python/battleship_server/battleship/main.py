import json

from twisted.web import server
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, task

from server.action import get_action
 
class BattleshipServer(Resource): 
    isLeaf = True
    def __init__(self):
        # throttle in seconds to check app for new data
        self.throttle = 0.1
        # define a list to store client requests
        self.delayed_requests = []
        # setup a loop to process delayed requests
        loopingCall = task.LoopingCall(self.processDelayedRequests)
        loopingCall.start(self.throttle, False)
        
        # initialize parent
        Resource.__init__(self)
 
    def render(self, request):
        """
        Handle a new request
        """
        print "accepting request"
        # set the request content type
        request.setHeader('Content-Type', 'application/json')
        # set args
        args = request.args
 
        # set jsonp callback handler name if it exists
        if 'callback' in args:
            request.jsonpcallback =  args['callback'][0]

        # get action and data
        action = get_action(request)
        if action:
            data = action.get_data()
            if len(data) > 0:
                return self.__format_response(request, data)
 
        # otherwise, put it in the delayed request list
        self.delayed_requests.append(request)
 
        # tell the client we're not done yet
        return server.NOT_DONE_YET
    
 
    def processDelayedRequests(self):
        """
        Processes the delayed requests that did not have
        any data to return last time around.
        """        
        # run through delayed requests
        for request in self.delayed_requests:
            try:
                # attempt to get data again
                action = get_action(request)
                if action:
                    data = action.get_data()
                    # write response and remove request from list if data is found
                    if len(data) > 0:
                        try:
                            request.write(self.__format_response(request, data))
                            request.finish()
                        except:
                            # Connection was lost
                            print 'connection lost before complete.'
                        finally:
                            # Remove request from list
                            self.delayed_requests.remove(request)
            except Exception, e:
                print 'exception while handling request - removing request'
                print str(e)
                self.delayed_requests.remove(request)
 
    def __format_response(self, request, data):
        """
        Format responses uniformly
        """
        # Set the response in a json format
        response = json.dumps({'data':data})
 
        # Format with callback format if this was a jsonp request
        if hasattr(request, 'jsonpcallback'):
            return request.jsonpcallback+'('+response+')'
        else:
            return response
        
def main():
    resource = BattleshipServer()
    factory = Site(resource)
    reactor.listenTCP(22483, factory)
    reactor.run()
 
#############################################       
if __name__ == '__main__':
    main()
    