from wsgiref.simple_server import make_server

from pyramid.config import Configurator


# this configures the app and runs it on the server
if __name__ == '__main__':
    # create the configuration object!
    config = Configurator()

    # DEBUG!!! REMOVE FOR PRODUCTION
    config.include('pyramid_debugtoolbar')
    # ------------------------------------

    config.include('pyramid_tm')

    # add all the routes
    config.add_route('index', '/')
    config.add_route('build', '/build')
    config.add_route('learn', '/learn')
    config.add_route('register', '/build/register')
    config.add_route('review', '/build/{topic}/review')
    config.add_route('reqs', '/build/{topic}/prerequisites')
    config.add_route('quiz', '/learn/{topic}/quiz')
    config.add_route('info', '/learn/{topic}/info')
    config.add_route('about', '/about')
    config.add_route('contact', '/contact')
    config.add_route('studies', '/studies')
    config.add_route('prereqs', '/prereq')
    config.add_route('prereqstart', '/prereq/start')
    config.add_route('next_req', '/prereq/{topic}')
    config.add_static_view(name='static', path='static')

    config.scan('views')                            # scan for views

    app = config.make_wsgi_app()                    # make the app
    server = make_server('0.0.0.0', 6543, app)      # pass app to server
    server.serve_forever()                          # run the server!
