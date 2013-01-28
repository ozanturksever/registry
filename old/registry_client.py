#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
try:
    import zmq
except:
    import zmqpy as zmq
try:
    import msgpack
except:
    import msgpack_pure as msgpack

class RegistryClient(object):
    def __init__(self):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
#        self.socket.setsockopt(zmq.RCVTIMEO, 1000)
        self.socket.connect('tcp://127.0.0.1:10000')
#        self.socket.connect('ipc:///tmp/10000')

    def get(self, key):
        self.socket.send(msgpack.packb({'action': 'get', 'params': {'key': key}}))
        data = self.socket.recv()
        return data

    def set(self, key, value):
        self.socket.send(msgpack.packb({'action': 'set', 'params': {'key': key,'value':value}}))
        resp = self.socket.recv()
        return resp

    def stat(self):
        self.socket.send(msgpack.packb({'action': 'stat'}))
