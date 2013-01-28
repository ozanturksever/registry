#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
try:
    import zmq
except ImportError:
    import zmqpy as zmq

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack


class Socket(object):
    def __init__(self, uri):
        self.uri = uri
        self.__connected = False

    def send(self, action, data=None):
        self.__connect()
        msg = msgpack.packb({'action': action, 'data': data})
        self.__socket.send(msg)
        response = self.__socket.recv()
        return msgpack.unpackb(response)

    def __connect(self):
        if self.__connected:
            return
        self.__ctx = zmq.Context()
        self.__socket = self.__ctx.socket(zmq.REQ)
        self.__socket.connect(self.uri)
        self.__connected = True


