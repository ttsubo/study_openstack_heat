import webob
import routes
import routes.middleware
import eventlet
from webob.dec import wsgify
from webob.exc import HTTPNotFound
from paste import httpserver
from paste.deploy import loadapp


class Router(object):
    def __init__(self, mapper):
        self.map = mapper
        self._router = routes.middleware.RoutesMiddleware(self._dispatch, self.map)

    @webob.dec.wsgify
    def __call__(self, req):
        return self._router

    @webob.dec.wsgify
    def _dispatch(self, req):
        match = req.environ['wsgiorg.routing_args'][1]
        if not match:
            return webob.exc.HTTPNotFound()
        app = match['controller']
        return app


class Resource(object):
    def __init__(self, controller):
        self.controller = controller

    @webob.dec.wsgify
    def __call__(self, request):
        action = self.get_action(request.environ)
        action_result = self.dispatch(self.controller, action, request)
        return webob.Response(action_result)

    def dispatch(self, obj, action, *args, **kwargs):
        method = getattr(obj, action)
        return method(*args, **kwargs)

    def get_action(self, request_environment):
        return request_environment['wsgiorg.routing_args'][1]['action']


class Server(object):
    def __init__(self, bind_host, bind_port):
        bind_addr = (bind_host, bind_port)
        self.sock = eventlet.listen(bind_addr)

    def start(self):
        self.pool = eventlet.GreenPool(size=100)
        self.pool.spawn_n(self._single_run, self.sock)

    def wait(self):
        self.pool.waitall()

    def _single_run(self, sock):
        eventlet.wsgi.server(sock,
                             loadapp('config:configured.ini', relative_to='.'),
                             custom_pool=self.pool,
                             debug=True)
