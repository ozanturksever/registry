#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from nose.tools import eq_
from src.registry import Registry

class TestRegistry:
    def setUp(self):
        self.r = Registry({
            'key0':'value0',
            'key_nasted0': {
                'key1':'value1'
            }
        })

    def test_get(self):
        value = self.r.get('key0')
        eq_(value, 'value0')
        value = self.r.get('key_nasted0')
        eq_(value, {'key1':'value1'})
        # must get copy of value
        value['key1']= 'other value'
        value = self.r.get('key_nasted0')
        eq_(value, {'key1':'value1'})

    def test_get_nasted(self):
        value = self.r.get('key_nasted0.key1')
        eq_(value, 'value1')

    def test_key_is_nasted(self):
        assert self.r.is_nasted('a.b')
        assert not self.r.is_nasted('a')
        assert not self.r.is_nasted(None)

    def test_extract_key(self):
        assert self.r.extract_key('a.b') == ['a','b']
        assert self.r.extract_key('a') == ['a']
        assert self.r.extract_key(None) == []

    def test_set(self):
        self.r.set('key', 'setted')
        value = self.r.get('key')
        eq_(value, 'setted')

    def test_set_nasted(self):
        self.r.set('a.b','c')
        value = self.r.get('a.b')
        eq_(value, 'c')
        self.r.set('x.y','z')
        value = self.r.get('x.y')
        eq_(value, 'z')

    def test_get_values(self):
        (version,values) = self.r.get_values()
        assert values['key0'] == 'value0'

    def test_set_values(self):
        self.r.set_values({'a':'b'})
        (version,values) = self.r.get_values()
        assert values == {'a':'b'}

    def test_set_values_with_version(self):
        self.r.set_values({'a':'b'}, 1)
        (version,values) = self.r.get_values()
        assert version == 1


    def test_get_version(self):
        assert self.r.get_version()

    def test_update_version_when_set(self):
        old_version = self.r.get_version()
        self.r.set('a','b')
        new_version = self.r.get_version()
        assert old_version != new_version

    def test_version_not_update_when_nothing_change(self):
        self.r.set('a','b')
        old_version = self.r.get_version()
        self.r.set('a','b')
        new_version = self.r.get_version()
        assert old_version == new_version

        self.r.set('x.y','z')
        old_version = self.r.get_version()
        self.r.set('x.y','z')
        new_version = self.r.get_version()
        assert old_version == new_version

    def test_update_version_when_set_values(self):
        old_version = self.r.get_version()
        self.r.set_values({'a':'b'})
        new_version = self.r.get_version()
        assert old_version != new_version
