#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import threading

import zmqpy as zmq
import zmqpy
import time
import msgpack_pure as msgpack


class MsgThread(threading.Thread):
    _exit = False

    def __init__(self, registry):
        self.registry = registry
        threading.Thread.__init__(self)

    def run(self):
        self.context = zmqpy.Context()
        self.socket = self.context.socket(zmq.PULL)
        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.setsockopt(zmq.SUBSCRIBE, '')
        self.socket.connect('tcp://127.0.0.1:10000')
        count = 0
        while not self._exit:
            try:
                msg = self.socket.recv()
                unpacked = msgpack.unpackb(msg)
                count+=1
                print count
#                print unpacked
#                if unpacked.get('action') == 'set':
#                    self.registry.set(unpacked.get('params', {}).get('key'), unpacked.get('params', {}).get('value'))
#                print self.registry.get(unpacked.get('params', {}).get('key'))
#                self.socket.send(msgpack.packb(self.registry.get(unpacked.get('params', {}).get('key'))))
            except zmq.ZMQError, err:
                pass
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
        self.msgThread = MsgThread(self)
        self.msgThread.start()

    def set(self, key, value):
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def stop_server(self):
        self.msgThread.exit()
        pass

    def __del__(self):
        if self.msgThread.is_alive:
            self.msgThread.exit()
