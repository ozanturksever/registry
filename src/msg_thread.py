#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from threading import Thread
import time
from src.interfaces.registry_server import IRegistryServer
from src.interfaces.server_socket import IServerSocket

try:
    import zmq
except ImportError:
    import zmqpy as zmq

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack


class MsgThread(Thread):
    _exit = False

    def __init__(self, registry, socket):
        if not isinstance(registry, IRegistryServer):
            raise Exception("registry must be IRegistryServer instance")
        if not isinstance(socket, IServerSocket):
            raise Exception("socket must be IServerSocket instance")

        self.registry = registry
        self.socket = socket

        Thread.__init__(self)

    def run(self):
        while not self._exit:
            msg = self.socket.recv()
            action = msg.get('action')
            if action == 'get':
                value = self.registry.get(msg.get('key'))
                self.socket.send(value)
            elif action == 'set':
                self.registry.set(msg.get('key'), msg.get('value'))
                self.socket.send(self.registry.get_version())
            elif action == 'commit':
                self.registry.commit(msg.get('data'))
                self.socket.send(self.registry.get_version())
            elif action == 'get_values':
                values = self.registry.get_values()
                self.socket.send(values)
            else:
                self.socket.send('unknown')
#            print "check",msg

    def exit(self):
        self._exit = True
