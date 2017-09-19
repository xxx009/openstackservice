import logging
import routes.middleware
import webob.dec
import webob.exc

"""Utility methods for working with WSGI servers."""

"""
https://github.com/openstack/nova/blob/master/nova/wsgi.py.Router()

nova.wsgi.Router, 
super class of nova.api.openstack.compute.APIRouterV21, 
uses routes.middleware.RoutesMiddleware internally to map incoming requests to these WSGI applications

"""

class Router(object):

    """ WSGI middleware that maps incoming requests to WSGI apps."""


    def __init__(self, mapper=None):

        """Create a router for the given routes.Mapper.
                Each route in `mapper` must specify a 'controller', which is a
                WSGI app to call.  You'll probably want to specify an 'action' as
                well and have your controller be an object that can route
                the request to the action-specific method.

                Examples:

                  mapper = routes.Mapper()
                  sc = ServerController()

                  # Explicit mapping of one route to a controller+action
                  mapper.connect(None, '/svrlist', controller=sc, action='list')

                  # Actions are all implicitly defined
                  mapper.resource('server', 'servers', controller=sc)
                  # Pointing to an arbitrary WSGI app.  You can specify the
                  # {path_info:.*} parameter so the target app can be handed just that
                  # section of the URL.
                  mapper.connect(None, '/v1.0/{path_info:.*}', controller=BlogApp())
        """

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

        """Dispatch the request to the appropriate controller.

                Called by self._router after matching the incoming request to a route
                and putting the information into req.environ.

                Either returns 404 or the routed WSGI app's response.
        """

        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app


