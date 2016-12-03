##http://docs.repoze.org/moonshining/pep333.html#example-application 

##* Simplest possible WSGI application
def simple_app(environ, start_response):
    """
    ##SM:Simplest Possible Application Object.
    ##SM:Our Application.
    """
    ##SM:HTTP status for the response
    status = '200 OK'
    ##SM:Construct HTTP response headers
    response_headers = [('Content-Type', 'text/plain')]
    start_response(status, response_headers)
    return ['Hello world!\n']

##SM:Server to serve Our Application "simple_app"
##Run server and serve the Application
if __name__ == '__main__':
    ##SM:Import http webserver from paste tool
    from paste import httpserver
    ##SM:Run our application "simple_app" under the Paste webserver
    httpserver.serve(simple_app, host='127.0.0.1', port='8080')

#Http REQUEST --> WSGI Server creates "environ" and "start_response" --> 
#calls Application (Example:simple_app) or Application's "__call__" if Application is an instance of a class --> 
#calls ``start_response`` with status and headers --> returns iterable