#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from mock import patch, MagicMock, Mock, call
import zmqpy
import msgpack_pure as msgpack

from registry import Registry
#from registry_stackless import Registry
#from registry_client import RegistryClient

class TestRegistry:
    zmq = Mock(spec=zmqpy)
    zmq.Context().socket().recv.return_value = msgpack.packb({'action': 'get', 'params': {'key': 'bla'}})

    @patch('registry.zmqpy', zmq)
    def test_can_construct(self):
    #        print self.zmq.Context()
        registry = Registry()
        registry.set('bla','hede')
        print self.zmq.Context().socket.call_count
        print self.zmq.Context().socket().recv.call_count
        print self.zmq.Context().socket().send.mock_calls[0] == call(msgpack.packb('hede'))
#        Mock().mock_calls
        #        assert registry
        registry.stop_server()

    #        print self.socketMock.call_count

#    def test_can_set_a_value(self):
#        registry = Registry()
#        registry.set('key', 'value')
#        assert registry.get('key') == 'value'
#        registry.stop_server()
#
#    def test_can_call_from_client(self):
#        registry = Registry()
#        registry.start_server()
