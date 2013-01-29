#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import json
from mock import patch, Mock, call
from src.persister import Persister
from src.registry import Registry

class TestPersister:
    def _prepare_mocks(self):
        self.open_mock = Mock()
        self.file_mock = Mock()
        self.file_mock.read.return_value = '{"a":"b","x":{"k0":"v0"}}'

        self.file_mock1 = Mock()
        self.file_mock1.read.return_value = '{"c":"d","x":{"k1":"v1"}}'

        self.export_file_mock = Mock()

        self.open_mock.side_effect = self._side_effect


    def _side_effect(self, arg, mode=None):
        if arg == '/tmp/registry.cfg':
            return self.file_mock
        if arg == '/tmp/registry1.cfg':
            return self.file_mock1
        if arg == '/tmp/registry_export.cfg' or 'output.cfg':
            return self.export_file_mock
        if arg == '/tmp/notexist.cfg':
            raise Exception('not exist')

    def setUp(self):
        self._prepare_mocks()
        self.patcher_open = patch('__builtin__.open', self.open_mock)
        self.patcher_open.start()
        self.p = Persister(['load0.cfg','load1.cfg'], 'output.cfg')

    def tearDown(self):
        self.patcher_open.stop()

    def test_load_from_file(self):
        self.p.load_file('/tmp/registry.cfg')
        assert self.p._Persister__registry.get('a') == 'b'
        assert self.file_mock.close.called

    def test_load_from_not_existed_file(self):
        self.p.load_file('/tmp/notexist.cfg')
        assert not self.p._Persister__registry.get_values()[1]

    def test_load_from_multiple_files(self):
        self.p.load_file('/tmp/registry.cfg')
        self.p.load_file('/tmp/registry1.cfg')
        assert self.p._Persister__registry.get('a') == 'b'
        assert self.p._Persister__registry.get('c') == 'd'
        assert self.p._Persister__registry.get('x')['k0'] == 'v0'
        assert self.p._Persister__registry.get('x')['k1'] == 'v1'

    def test_export_to_file(self):
        self.p._Persister__registry.set('a','b')
        self.p.export('/tmp/registry_export.cfg')
        assert self.export_file_mock.write.call_args == call(json.dumps({'a':'b'},indent=4))
        assert self.export_file_mock.close.called

    def test_export_defaults_to_output_file(self):
        self.p.export()
        assert self.open_mock.call_args == call('output.cfg','w')

    def test_loads_cfg_on_init(self):
        assert self.open_mock.call_args_list == [call('load0.cfg'), call('load1.cfg')]

    def test_set_registry(self):
        self.p.set_registry_values({'x':'y'})
        assert self.p._Persister__registry.get('x') == 'y'

    def test_get_values(self):
        assert self.p.get_values()

