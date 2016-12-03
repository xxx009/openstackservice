#http://docs.repoze.org/moonshining/tools/paste.html#exercise-configuring-an-application

##Our Application "OurApplication.py"

class OurApplication:
    def __init__(self, name, greeting):
        self.name = name
        self.greeting = greeting
    def __call__(self, environ, start_response):
        status = '200 OK'
        response_headers = [('Content-Type', 'text/plain')]
        start_response(status, response_headers)
        return ['%s, %s!\n' % (self.greeting, self.name)]

##factory method to get Our Application via .ini file
def app_factory(global_config, name='Johnny', greeting='Howdy'):
    return OurApplication(name, greeting)

if __name__ == '__main__':
    from paste import httpserver
    from paste.deploy import loadapp
    httpserver.serve(loadapp('config:configured.ini', relative_to='.'),
                     host='127.0.0.1', port='8080')