#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from mock import Mock, patch, call
from src.registry_server import RegistryServer

class TestRegistryServer:
    def setUp(self):
        self.server_socket_mock = Mock()
        self.msg_thread_mock = Mock()
        self.patcher = patch('src.registry_server.ServerSocket', self.server_socket_mock)
        self.msg_thread_patcher = patch('src.registry_server.MsgThread', self.msg_thread_mock)
        self.patcher.start()
        self.msg_thread_patcher.start()
        self.s = RegistryServer({'a':'b'})

    def tearDown(self):
        self.patcher.stop()
        self.msg_thread_patcher.stop()

    def test_get(self):
        value = self.s.get('a')
        assert value == 'b'

    def test_set(self):
        self.s.set('a','c')
        value = self.s.get('a')
        assert value == 'c'

    def test_remove(self):
        self.s.set('a','c')
        self.s.remove('a')
        assert not self.s.get('a')

    def test_commit(self):
        self.s.commit({'a':'b','c':'d'})
        assert self.s._RegistryServer__registry.get_values()[1] == {'a':'b','c':'d'}

    def test_get_values(self):
        self.s.commit({'a':'b'})
        assert self.s.get_values()[1] == {'a':'b'}

    def test_listens(self):
        assert self.s.socket

    def test_msg_thread_started(self):
        assert self.msg_thread_mock.called
        assert self.msg_thread_mock.call_args[0][0] == self.s
        assert self.msg_thread_mock.call_args[0][1] == self.s.socket
        assert self.msg_thread_mock().start.called

    def test_calls_callback_when_changed(self):
        refresh_func_mock = Mock()

        c = RegistryServer({}, refresh_callback=refresh_func_mock)
        c.set('a','b')
        assert refresh_func_mock.called
        assert refresh_func_mock.call_args == call(c)

        refresh_func_mock.reset_mock()
        c = RegistryServer({}, refresh_callback=refresh_func_mock)
        c.set('a','b')
        c.remove('a')
        assert refresh_func_mock.called

        refresh_func_mock.reset_mock()
        c = RegistryServer({}, refresh_callback=refresh_func_mock)
        c.commit({})
        assert refresh_func_mock.called

