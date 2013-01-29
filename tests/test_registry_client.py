#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from mock import Mock, patch
from nose.tools import eq_
from src.registry_client import RegistryClient
import time

class TestRegistryClient:
    def setUp(self):
        self.socket_mock = Mock()
        self.socket_mock().send.return_value = (1,{'key':'value','a':{'b':'val'}})
        self.patcher = patch('src.registry_client.Socket', self.socket_mock)
        self.patcher.start()
        self.client = RegistryClient()

    def tearDown(self):
        self.patcher.stop()

    def test_get(self):
        value = self.client.get('key')
        eq_(value, 'value')
        value = self.client.get('a')
        eq_(value, {'b':'val'})
        # must get copy of value
        value['b']= 'c'
        value = self.client.get('a')
        eq_(value, {'b':'val'})

    def test_get_nasted(self):
        value = self.client.get('a.b')
        eq_(value, 'val')

    def test_set(self):
        self.client.set('key', 'setted')
        value = self.client.get('key')
        eq_(value, 'setted')

    def test_set_nasted(self):
        self.client.set('a.b','c')
        value = self.client.get('a.b')
        eq_(value, 'c')
        self.client.set('x.y','z')
        value = self.client.get('x.y')
        eq_(value, 'z')

    def test_remove(self):
        self.client.set('key', 'setted')
        value = self.client.remove('key')
        assert not value

    def test_commit(self):
        self.socket_mock().send.return_value = 1
        self.client.set('key1','value1')
        self.client.commit()
        assert self.socket_mock().send.call_args[0] == ('commit',self.client._RegistryClient__registry.get_values()[1])
        assert self.client._RegistryClient__registry.get_version() == 1

    def _setup_mock_for_periodically_update(self):
        values = [
            (2,{'key':'value','a':{'b':'val'}}),
            (1,{'key':'value','a':{'b':'val'}})
        ]
        def return_values(arg):
            if arg == 'get_values':
                return values.pop()
            if arg == 'get_version':
                return 2
        self.socket_mock().send.side_effect = return_values

    def test_update_periodically(self):
        self._setup_mock_for_periodically_update()
        c = RegistryClient(update_period=0.01)
        time.sleep(0.02)
        assert c._RegistryClient__registry.get_version() == 2

    def test_calls_callback_when_refresh(self):
        self._setup_mock_for_periodically_update()
        refresh_func_mock = Mock()

        c = RegistryClient(update_period=0.01, refresh_callback=refresh_func_mock)
        time.sleep(0.02)
        assert refresh_func_mock.called

