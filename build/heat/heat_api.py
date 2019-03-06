import os
import time
import logging
import oslo.messaging
import webob
import routes
import routes.middleware
import eventlet
import eventlet.wsgi
from wsgi import Resource, Router, Server
from webob.dec import wsgify
from webob.exc import HTTPNotFound
from paste import httpserver
from paste.deploy import loadapp
from oslo.config import cfg

CONF = cfg.CONF
CONF(default_config_files=['conf/heat.conf'])

oslo.messaging.set_transport_defaults('heat')
TRANSPORT = oslo.messaging.get_transport(CONF)
ENGINE_TOPIC = 'engine'

bind_host = "0.0.0.0"
bind_port = 8080

def get_rpc_client(**kwargs):
    target = oslo.messaging.Target(**kwargs)
    return oslo.messaging.RPCClient(TRANSPORT, target)


class EngineClient(object):

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self):
        self._client = get_rpc_client(
            topic=ENGINE_TOPIC,
            version=self.BASE_RPC_API_VERSION)

    @staticmethod
    def make_msg(method, **kwargs):
        return method, kwargs

    def call(self, ctxt, msg, version=None):
        method, kwargs = msg
        if version is not None:
            client = self._client.prepare(version=version)
        else:
            client = self._client
        return client.call(ctxt, method, **kwargs)

    def hello(self, ctxt, seqid, host, content):
        return self.call(ctxt, self.make_msg("hello",
                                             seqid=seqid,
                                             host=host,
                                             req=content))

    def goodbye(self, ctxt, seqid, host, content):
        return self.call(ctxt, self.make_msg("goodbye",
                                             seqid=seqid,
                                             host=host,
                                             req=content))


class Configured(Router):
    def __init__(self, name, greeting):
        mapper = routes.Mapper()

        stacks_resource = Resource(StackController(name, greeting))
        with mapper.submapper(controller=stacks_resource,
                              path_prefix="/greeting") as stack_mapper:
            stack_mapper.connect("stack_index",
                                 "/hello",
                                 action="hello",
                                 conditions={'method': 'GET'})

            stack_mapper.connect("stack_index",
                                 "/goodbye",
                                 action="goodbye",
                                 conditions={'method': 'GET'})

        super(Configured, self).__init__(mapper)


class StackController(object):
    def __init__(self, name, greeting):
        self.rpc_client = EngineClient()
        self.name = name
        self.greeting = greeting
        self.sequence_id = 0

    def hello(self, req):
        self.sequence_id += 1
        myhost = os.uname()[1]
        content = "How are you?"
        (id, hostname, response) = self.rpc_client.hello({}, self.sequence_id, myhost, content)
        logging.info("### Response: id=[{0}], host=[{1}], content=[{2}]"
                    .format(id, hostname, response))
        return "%s, %s, %s !!\n" % (response, self.greeting, self.name)

    def goodbye(self, req):
        self.sequence_id += 1
        myhost = os.uname()[1]
        content = "Good bye!"
        (id, hostname, response) = self.rpc_client.goodbye({}, self.sequence_id, myhost, content)
        logging.info("### Response: id=[{0}], host=[{1}], content=[{2}]"
                    .format(id, hostname, response))
        return "%s, %s, %s !!\n" % (response, self.greeting, self.name)


def app_factory(global_config, name='Johnny', greeting='Howdy'):
    return Configured(name, greeting)


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                        level=logging.DEBUG)

    server = Server(bind_host, bind_port)
    server.start()
    server.wait()
