#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import threading
import stackless

import zmqpy as zmq
import time
import msgpack_pure as msgpack


class msgThread(object):
    _exit = False

    def __init__(self, registry):
        self.registry = registry
        stackless.tasklet(self.run)()

    def run(self):
        print "running"
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.bind('tcp://127.0.0.1:10000')
        while not self._exit:
            try:
                msg = self.socket.recv()
                unpacked = msgpack.unpackb(msg)
                if unpacked.get('action') == 'set':
                    self.registry.set(unpacked.get('params', {}).get('key'), unpacked.get('params', {}).get('value'))
                self.socket.send(self.registry.get(unpacked.get('params', {}).get('key')))
            except zmq.ZMQError, err:
                pass
            stackless.schedule()
        self._close_socket()

    def _close_socket(self):
        if not self.socket.closed:
            self.socket.close()
        if not self.context.closed:
            self.context.term()
        pass

    def exit(self):
        self._exit = True

class Registry(object):
    data = {}
    server_started = False
    _stop_server = False

    def __init__(self):
        self.msgThread = msgThread(self)

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def stop_server(self):
        self.msgThread.exit()

    def __del__(self):
        if self.msgThread.is_alive:
            self.msgThread.exit()

