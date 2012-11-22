from twisted.web import server
from twisted.web.server import Site
from twisted.web.resource import Resource
from twisted.internet import reactor, task
import json
 
class BattleshipServer(Resource): 
    isLeaf = True
    def __init__(self):
        # throttle in seconds to check app for new data
        self.throttle = 1
        # define a list to store client requests
        self.delayed_requests = []
        # setup a loop to process delayed requests
        loopingCall = task.LoopingCall(self.processDelayedRequests)
        loopingCall.start(self.throttle, False)
        
        self.users = {}
        self.update_key = 0
        
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

        if 'user' in args:
            user = args['user'][0]
            request.lastupdate = self.users.get(user, {}).get('updated', 0)
            request.user = user
            self.addUser(user)
            data = self.getUserList(request,  user)
        else:
            data = []
        if len(data) > 0:
            return self.__format_response(request, data)
 
        # otherwise, put it in the delayed request list
        self.delayed_requests.append(request)
 
        # tell the client we're not done yet
        return server.NOT_DONE_YET
    
    def addUser(self, user):
        if not user in self.users.keys():
            self.update_key += 1
            self.users[user] = {'name':user}
 
    def getUserList(self, request, user):
        """
        Replace this logic with code that will actually test for
        and return data your app should return.
 
        You can use request.lastupdate here if you want to pull
        data since the last time this request received data.
 
        This is just dummy logic to make this demo work.
        """
        # init data
        data = {}
        if request.lastupdate != self.update_key:           # you can dynamically add any key/value pair here
            data = {'users':self.users.values()}
            self.users[request.user]['updated'] = self.update_key
 
        return data
 
    def processDelayedRequests(self):
        """
        Processes the delayed requests that did not have
        any data to return last time around.
        """        
        # run through delayed requests
        for request in self.delayed_requests:
            # attempt to get data again
            data = self.getUserList(request, request.user)
 
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
    