#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from mock import Mock, patch
from nose.tools import eq_
from src.registry_client import RegistryClient

class TestRegistryClient:
    def setUp(self):
        self.socket_mock = Mock()
        self.socket_mock().send.return_value = {'key':'value','a':{'b':'val'}}
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


    def test_commit(self):
        self.client.set('key1','value1')
        self.client.commit()
        assert self.socket_mock().send.call_args[0] == ('commit',self.client._RegistryClient__registry.get_values())
