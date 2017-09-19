import routes

from restapi import wsgi
from restapi import servers

""" 
https://github.com/openstack/nova/blob/master/nova/api/openstack/compute/routes.py

"""

class APIRouterV21(wsgi.Router):

    """Routes requests on the OpenStack API to the appropriate controller and method.

     Explicit mapping of one route to a controller+action is build at here
     mapper.connect(None, '/svrlist', controller=sc, action='list')

    """

    def __init__(self, mapper=None):
        if(mapper == None):
            mapper = routes.Mapper()
        
        versions_resource = servers.create_resource()
        mapper.connect("/",controller=versions_resource,action="index")
        super(APIRouterV21,self).__init__(mapper)

#How to relate  /v2/project_id/servers/ to nova.api.openstack.compute.servers.Controller.index()