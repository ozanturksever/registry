#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from mock import Mock, patch

from src.server_socket import ServerSocket
try:
    import zmq
except ImportError:
    import zmqpy as zmq

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack

class TestServerSocket:
    def setUp(self):
        self.zmq_mock = Mock(spec=zmq)
        self.zmq_mock.Context().socket().recv.return_value = msgpack.packb({'a':'b'})
        self.patcher = patch('src.server_socket.zmq', self.zmq_mock)
        self.patcher.start()
        self.s = ServerSocket('tcp://127.0.0.1:10000')

    def tearDown(self):
        self.patcher.stop()

    def test_bind(self):
        self.s._ServerSocket__bind()
        assert self.zmq_mock.Context.called
        assert self.zmq_mock.Context().socket().bind.call_args[0] == (('tcp://127.0.0.1:10000'),)

    def test_recv(self):
        value = self.s.recv()
        assert value == {'a':'b'}

    def test_send(self):
        self.s.send({'a':'b'})
        assert self.zmq_mock.Context().socket().send.called
        assert self.zmq_mock.Context().socket().send.call_args[0][0] == msgpack.packb({'a':'b'})



