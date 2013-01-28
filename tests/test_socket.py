#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from mock import patch, Mock
from src.socket import Socket

try:
    import zmq
except ImportError:
    import zmqpy as zmq

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack


class TestSocket:
    def setUp(self):
        self.zmq_mock = Mock(spec=zmq)
        self.zmq_mock.Context().socket().recv.return_value = msgpack.packb({'a':'b'})
        self.patcher = patch('src.socket.zmq', self.zmq_mock)
        self.patcher.start()
        self.s = Socket('tcp://127.0.0.1:10000')

    def tearDown(self):
        self.patcher.stop()

    def test_connect(self):
        self.s._Socket__connect()
        assert self.zmq_mock.Context.called
        assert self.zmq_mock.Context().socket().connect.call_args[0] == (('tcp://127.0.0.1:10000'),)

    def test_send(self):
        self.s.send('get_all')
        assert self.zmq_mock.Context().socket().send.called
        assert self.zmq_mock.Context().socket().send.call_args[0] == (msgpack.packb({'action':'get_all','data':None}),)

    def test_recv(self):
        value = self.s.send('get_all')
        assert self.zmq_mock.Context().socket().recv.called
        assert value == {'a':'b'}

    def test_send_with_data(self):
        self.s.send('commit',{'a':'b'})
        assert self.zmq_mock.Context().socket().send.called
        assert self.zmq_mock.Context().socket().send.call_args[0] == ((msgpack.packb({'action':'commit','data':{'a':'b'}})),)
