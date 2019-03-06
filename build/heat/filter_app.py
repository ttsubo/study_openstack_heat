import webob
from webob.dec import wsgify
from webob import exc


class Middleware(object):
    def __init__(self, application):
        self.application = application

    def process_response(self, response):
        return response

    @webob.dec.wsgify
    def __call__(self, req):
        response = self.process_request(req)
        if response:
            return response
        response = req.get_response(self.application)
        return self.process_response(response)


class AuthFilter(Middleware):
    def __init__(self, application):
        super(AuthFilter, self).__init__(application)

    def process_request(self, request):
        if request.headers.get('X-Auth-Token') != 'open-sesame':
            return exc.HTTPForbidden()
        return request.get_response(self.application)


class OutputToken(Middleware):
    def __init__(self, application):
        super(OutputToken, self).__init__(application)

    def process_request(self, request):
        x_auth_token = request.headers.get('X-Auth-Token')
        print("Receiving Request: [X-Auth-Token]=\"%s\"" % x_auth_token)
        return None


def auth_filter_factory(global_config, **local_config):

    def filter(app):
        return AuthFilter(app)
    return filter


def output_filter_factory(global_config, **local_config):
    def filter(app):
        return OutputToken(app)
    return filter
