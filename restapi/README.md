
 - WSGI Server    
 code: openstackservice/restapi/restapi/service.py    
 功能：
 
        1：启动wsgi server， 接受api请求        
        2：Past deploy加载wsgi Application  
        
 - WSGI Application    
 code：openstackservice/restapi/restapi/servers.py    
 功能：
 
       1：Rest API的具体实现    
    
 - WSGI Middleware    
 code：openstackservice/restapi/restapi/router.py 
       openstackservice/restapi/restapi/wsgi.py    
 功能:
       
       router.py 定义各种url和controller直接的影射关系，最终由wsgi.py的类Router加载这些mapper    
       
        1：构造url到资源的映射，路由规则的创建    
        2：资源的加载    
          3：Rest API请求路由到正确的WSGI Application    
          
   
 - paste-api.ini  
 
        [app:restapi]    
        paste.app_factory = restapi.router:APIRouterV21.factory    


- 调用顺序  

      router.API.__init__()    
      wsgi.Router.__init__()    
      wsgi.Router.call()    
      wsgi.Router.__dispatch()        
      servers.Controller.call()    
      servers.Controller.index()        

----------
wsgi.Router它负责分发HTTP Request到其管理的某个Resource.    

 - 属性resources是个数组，用来保存所有的Resource的Controller类的instance；每个Resource拥有一个该数组的数组项，比如self.resources['versions'] =versions.create_resource()会为versions核心资源创建一个Resource并保存到resources中。
 
 - 属性mapper用来保存保存所有resource的routes供RoutesMiddleware使用。它其实是一张路由表。每个表项表示一个URL和controller以及action的映射关系
 
 - 属性routes是routes.middleware.RoutesMiddleware的实例，它其实是一个WSGIapp，它使用mapper和 _dispatch_进行初始化。功能是根据URL得到 controller和它的action。

在service启动阶段，通过paste deploy调用restapi.router:API.factory
router.py的__init__方法被调用，加载资源，建立资源的路由表，然后把生成的mapper传给初始化了的routes.middleware.RoutesMiddleware。

在处理HTTP Request阶段，它负责接收经过Middleware filters处理过的HTTP Request，再把它转发给RoutesMiddleware实例，它会使用mapper得到 Request的URL对应的controller和action，并设置到Request的environ中，然后再调用APIRoutes的dispatch方法。该方法会从environ中得到controller，然后调用其 __call_ 方法，实现消息的分发。

----------
* How to run?
'''python server.py'''
* How to access
localhost:8080

* How to build package
'python setup.py sdist'

