import logging
import routes.middleware
import webob.dec
import webob.exc


class Router(object): 

    def __init__(self, mapper=None):
        self.map =  mapper 
        self._router = routes.middleware.RoutesMiddleware(self._dispatch,
                                                         self.map) 
    @classmethod
    def factory(cls, global_conf, **local_conf): 
        return cls() 

    @webob.dec.wsgify 
    def __call__(self,req): 
        return self._router

    @staticmethod
    @webob.dec.wsgify
    def _dispatch(req):
        # TODO
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app
