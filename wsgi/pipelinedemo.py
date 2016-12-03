#!/usr/bin/python
#encoding: utf-8

import os
import eventlet
from eventlet import wsgi, listen
from paste import deploy
from webob import Request

cfg_file = 'paste-api.ini'
server_list = [('blog', 8001), ('wiki', 8002), ]


class Blog(object):
    def __init__(self):
        pass

    # 工厂函数, ini 配置文件中指定的值会找到这个函数来创建该 app 的实例
    @classmethod
    def factory(cls, global_conf, **local_conf):
        return cls()

    # python 的对象调用机制, 简单的来讲就是 python 中对象分为可调用的和不可调用的
    # 有 __call__ 方法的可以调用, 这样 ini 中指定的配置项的值调用的时候就直接调用到
    # 这个函数了
    def __call__(self, environ, start_response):
        # start_response 把用户传递的 HTTP status 和 headers 记录然后返回
        start_response('200 OK', {("Content-type", "text/plain")})
        return 'welcome to my blog\n'
blog_app = Blog.factory


class Wiki(object):
    def __init__(self):
        pass

    @classmethod
    def factory(cls, global_conf, **local_conf):
        return cls()

    def __call__(self, environ, start_response):
        start_response('200 OK', {("Content-type", "text/plain")})
        return 'welcome to my wiki\n'


class Middleware(object):
    def __init__(self, app):
        self.app = app

    @classmethod
    def factory(cls, global_conf, **kwargs):
        def filter(app):
            return cls(app)
        return filter


class WikiFilter(Middleware):
    def __init__(self, app):
        super(WikiFilter, self).__init__(app)

    def __call__(self, environ, start_response):
        req = Request(environ)
        if req.method == 'PUT':
            start_response('200 OK', {("Content-type", "text/plain")})
            return 'Bad request\n'
        else:
            return self.app(environ, start_response)


class LogIPFilter(Middleware):
    def __init__(self, app):
        super(LogIPFilter, self).__init__(app)

    def __call__(self, environ, start_response):
        print 'request IP is: %s' % environ['REMOTE_ADDR']
        return self.app(environ, start_response)


class LogMethodFilter(Middleware):
    def __init__(self, app):
        super(LogMethodFilter, self).__init__(app)

    def __call__(self, environ, start_response):
        print 'request method is: %s' % environ['REQUEST_METHOD']
        return self.app(environ, start_response)


class V1(object):
    @classmethod
    def factory(cls, global_conf, **local_conf):
        return cls()

    def __call__(self, environ, start_response):
        start_response('200 OK', {("Content-type", "text/plain")})
        return 'welcome to my V1 wiki\n'

if __name__ == '__main__':
    host = '0.0.0.0'
    servers = []
    for app_name, port in server_list:
        socket = listen((host, port))
        # paste 提供的入口函数
        app = deploy.loadapp('config:%s' % os.path.abspath(cfg_file), app_name)

        print "%s is starting" % app_name
        servers.append(eventlet.spawn(wsgi.server, socket, app))

    for server in servers:
        server.wait()
