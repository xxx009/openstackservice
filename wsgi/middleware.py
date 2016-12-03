
class Caseless:
    """
        Creates a middleware as class.
        Class as a middleware component.
    """
    def __init__(self, app):

        self.app = app

    def __call__(self, environ, start_response):
        """
            WSGI Architecture for Application.
            WSGI application interface.
            So this will act as an application.
        """
        ##Call Out Application and convert result to lowercase and return
        for chunk in self.app(environ, start_response):
            yield chunk.lower()

##Run server and serve the Application "simple_app"
if __name__ == '__main__':
    from paste import httpserver
    from app import simple_app
    ##Calls the middleware "Caseless"
    httpserver.serve(Caseless(simple_app), host='127.0.0.1', port='8080')
