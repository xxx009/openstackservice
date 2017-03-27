
 - WSGI Server    
 code: openstackservice/restapi/restapi/server.py    
 功能：
        1：启动wsgi server， 接受api请求        
        2：Past deploy加载wsgi Application  
        
 - WSGI Application    
 code：openstackservice/restapi/restapi/versions.py    
 功能：    
       1：Rest API的具体实现    
    
 - WSGI Middleware    
 code：openstackservice/restapi/restapi/router.py    
       openstackservice/restapi/restapi/wsgi.py    
 功能：    
   1：构造url到资源的映射，路由规则的创建    
   2：资源的加载    
   3：Rest API请求路由到正确的WSGI Application    
   
 - paste-api.ini    
  [app:restapi]    
  paste.app_factory = restapi.router:API.factory    


调用顺序
router.API.__init__()
wsgi.Router.__init__()
wsgi.Router.call()
wsgi.Router.__dispatch()
versions.Controller.call()
versions.Controller.index()

----------
wsgi.Router它负责分发 HTTP Request 到其管理的某个 Resource.    

 - 属性 resources 是个数组，用来保存所有的 Resource 的 Controller 类的instance；每个Resource拥有一个该数组的数组项，比如self.resources['versions'] =versions.create_resource() 会为 versions 核心资源创建一个 Resource 并保存到resources 中。
 
 - 属性 mapper 用来保存保存所有 resource的 routes 供 RoutesMiddleware 使用。它其实是一张路由表。每个表项表示一个 URL 和 controller 以及 action 的映射关系
 
 - 属性 routes 是 routes.middleware.RoutesMiddleware 的实例，它其实是一个 WSGIapp，它使用 mapper 和 _dispatch_进行初始化。功能是根据 URL 得到 controller 和它的 action。

在service启动阶段，通过paste deploy调用restapi.router:API.factory
router.py的 __init__ 方法被调用，加载资源，建立资源的路由表，然后把生成的 mapper 传给初始化了的 routes.middleware.RoutesMiddleware。

在处理 HTTP Request 阶段，它负责接收经过 Middleware filters 处理过的 HTTP Request，再把它转发给 RoutesMiddleware 实例，它会使用 mapper 得到 Request 的URL 对应的 controller 和 action，并设置到 Request 的 environ 中，然后再调用 APIRoutes 的 dispatch 方法。该方法会从 environ 中得到controller，然后调用其 __call_ 方法，实现消息的分发。

----------
* How to run?
'''python server.py'''
* How to access
localhost:8080

* How to build package
'python setup.py sdist'

