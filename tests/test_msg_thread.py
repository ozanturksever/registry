#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import time
from mock import Mock, call
from src.interfaces.registry_server import IRegistryServer
from src.interfaces.server_socket import IServerSocket
from src.msg_thread import MsgThread

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack

class TestMsgThread:
    def setUp(self):
        self.registry_server_mock = Mock(spec=IRegistryServer)
        self.socket = Mock(spec=IServerSocket)
        self.m = MsgThread(self.registry_server_mock, self.socket)

    def test_run(self):
        self.m.start()
        time.sleep(0.001)
        self.m.exit()
        assert self.socket.recv.called

    def test_get(self):
        self.socket.recv.return_value = {'action':'get','key':'a'}
        self.registry_server_mock.get.return_value = 'value'
        self.m.start()
        time.sleep(0.001)
        self.m.exit()
        assert self.registry_server_mock.get.call_args == call('a')
        assert self.socket.send.call_args == call('value')

    def test_set(self):
        self.socket.recv.return_value = {
            'action':'set',
            'key':'a',
            'value':'value'
        }
        self.m.start()
        time.sleep(0.001)
        self.m.exit()
        assert self.registry_server_mock.set.call_args == call('a','value')
        assert self.socket.send.call_args == call('saved')

    def test_commit(self):
        self.socket.recv.return_value = {
            'action':'commit',
            'data':{'a':'b','c':'d'}
        }
        self.m.start()
        time.sleep(0.001)
        self.m.exit()
        assert self.registry_server_mock.commit.call_args == call({'a':'b','c':'d'})
        assert self.socket.send.call_args == call('saved')

    def test_get_values(self):
        self.socket.recv.return_value = {
            'action':'get_values'
        }
        self.m.start()
        time.sleep(0.001)
        self.m.exit()
        assert self.registry_server_mock.get_values.called
        assert self.socket.send.called
