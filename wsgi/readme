## WSGI Server/gateway

wsgi server可以理解为一个符合wsgi规范的web server，接收request请求，封装一系列环境变量，按照wsgi规范调用注册的wsgi app，最后将response返回给客户端。文字很难解释清楚wsgi server到底是什么东西，以及做些什么事情，最直观的方式还是看wsgi server的实现代码。以python自带的wsgiref为例，wsgiref是按照wsgi规范实现的一个简单wsgi server。
### wsgi server 基本工作流程

-  服务器创建socket，监听端口，等待客户端连接。
-  当有请求来时，服务器解析客户端信息放到环境变量environ中，并调用绑定的handler来处理请求。
- handler解析这个http请求，将请求信息例如method，path等放到environ中。
-  wsgi handler再将一些服务器端信息也放到environ中，最后服务器信息，客户端信息，本次请求信息全部都保存到了环境变量environ中。
-   wsgi handler 调用注册的wsgi app，并将environ和回调函数传给wsgi app
 wsgi app 将reponse header/status/body 回传给wsgi handler
-  最终handler还是通过socket将response信息塞回给客户端。

## WSGI Application
wsgi application就是一个普通的callable对象，当有请求到来时，wsgi server会调用这个wsgi app。这个对象接收两个参数，通常为environ,start_response。environ就像前面介绍的，可以理解为环境变量，跟一次请求相关的所有信息都保存在了这个环境变量中，包括服务器信息，客户端信息，请求信息。start_response是一个callback函数，wsgi application通过调用start_response，将response headers/status 返回给wsgi server。此外这个wsgi app会return 一个iterator对象 ，这个iterator就是response body。这么空讲感觉很虚，对着下面这个简单的例子看就明白很多了。
###  下面这个例子是一个最简单的wsgi app，
 引自http://www.python.org/dev/peps/pep-3333/


```
def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [u"This is hello wsgi app".encode('utf8')]
```


我们再用wsgiref 作为wsgi server ，然后调用这个wsgi app，就能直观看到一次request,response的效果，简单修改代码如下：


```
from wsgiref.simple_server import make_server

def simple_app(environ, start_response):
    status = '200 OK'
    response_headers = [('Content-type', 'text/plain')]
    start_response(status, response_headers)
    return [u"This is hello wsgi app".encode('utf8')]

httpd = make_server('', 8000, simple_app)
print "Serving on port 8000..."
httpd.serve_forever()
```


访问http://127.0.0.1:8000 就能看到效果了。

---
## Paste配置文件
配置文件分为多个section，每个section的名字的格式是TYPE:NAME，每个section中参数的格式一般是KEY = VALUE。我们分别来看看各种TYPE

- TYPE = composite

```
[composite:wiki]
         use = egg:Paste#urlmap
         /: home
         /v1: wikiv1
```


composite这个类型的section会的把具体的URL请求分配到VALUE对应的section中的APP上去。use表明具体的分配方法，换句话说这里的KEY = VALUE是egg:Paste#urlmap这个Python模块的参数， egg:Paste#urlmap的实现应该类似于：

```
if (URL == "/") call(home_app)
if (URL == "/wikiv1") call(wiki)
```


- TYPE = app

```
[app:homeapp]
   paste.app_factory = app:wiki.factory
```


一个app就是一个具体的WSGI的应用。具体调用那个python module中的app则由use来指定。这里直接指定了使用app 中的:Wiki.factory作为我们的app    
•	Line 1 begins a section with the app: prefix, used to define a WSGI application endpoint. The name homeapp makes this application the default for this file.    
•	Line 2 tells PasteDeploy to look up the function wiki_factory in the module app, and call it to get the application.
- TYPE = filter-app

```
[filter-app:home]
   paste.filter_factory = app:WikiFilter.factory
   next = homeapp
```


filter-app就是一个过滤，也就是说一个请求过来后，会的先走filter-app中的use指定的app，如果那个app过滤了这个request，那么这个request就不会发送到next指定的app中去进行下一步处理了。如果没有过滤，则会发送给next指定的app。这个filter-app虽然有过滤的名字，但其实也不一定要做过滤这档子事情，可以用来记录些日志啥的，比如每次来个请求就log些东西，然后再转给后面的app去处理。fiter-app必须要有next，这个和filter不一样    
•	Line 1 defines the filter. by default, no filters are included: they must be explicitly configured.    
•	Line 2 tells PasteDeploy to look up the function WikiFilter.factory in the module app, and call it to get the filter.

- TYPE = filter

```
[filter:logip]
    paste.filter_factory = app:LogIPFilter.factory
```


  和filter-app差不多，但是没有next

- TYPE = pipeline

```
[pipeline:wikiv1]
   pipeline = logip logmethod v1
```


pipeline就是简化了filter-app，不然你想，如果我有十个filter，那不是要写十个filter-app，然后用next连起来？所以通过pipeline，我就可以把这些filter都连起来写在一行，很方便。但要注意的是这些filter需要有一个app作为结尾。

### 基本用法
如何使用呢？很简单。我们都说了，这个Paste Deploy就是为了从配置文件生成一个WSGI的APP，所以只要这样调用就行了


```
from paste.deploy import loadapp
wsgi_app = loadapp('config:/path/to/config.ini')
```


### factory格式
PasteDeploy自身有很多的factory，这些factory对普通的WSGI标准做了个封装，让用的时候好用一些
