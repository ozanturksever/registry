#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from src.interfaces.server_socket import IServerSocket

try:
    import zmq
except ImportError:
    import zmqpy as zmq

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack

class ServerSocket(object, IServerSocket):
    def __init__(self, uri):
        self.uri = uri
        self.__bind()

    def recv(self):
        msg = self.__socket.recv()
        decoded_msg = msgpack.unpackb(msg)
        return decoded_msg

    def send(self, msg):
        encoded_msg = msgpack.packb(msg)
        self.__socket.send(encoded_msg)

    def __bind(self):
        self.__ctx = zmq.Context()
        self.__socket = self.__ctx.socket(zmq.REP)
        self.__socket.bind(self.uri)
