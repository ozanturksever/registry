#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from registry_client import RegistryClient
#from registry_client_pub import RegistryClient
import sys
import timeit

c = RegistryClient()


mcount=0
def set_a():
    global  mcount
    mcount+=1
    c.set('a','++++++++++++++++++++++++')

def get_a():
    c.get('a')

def test_get():
    count = 100000
    setup = 'from __main__ import set_a'
    test_code = 'set_a()'
    total_time = timeit.timeit(test_code, setup=setup, number=count)
    print "total:",total_time
    print "r/s:", count/total_time, 'mcount:',mcount
    c.stat()
    c.stat()
    c.stat()
    c.stat()

def test_json_vs_msgpack():
#    count = 100000
    count = 100000
    setup = 'import json'
    test_code = 'a={"a":"b","c":{"d":"e","f":1000}}; j = json.dumps(a); j2 = json.loads(j)'
    total_time = timeit.timeit(test_code, setup=setup, number=count)
    print "json:"
    print "total:",total_time
    print "r/s:", count/total_time
    print "msgpack:"
    setup = 'import msgpack_pure as msgpack'
    test_code = 'a={"a":"b","c":{"d":"e","f":1000}}; msg = msgpack.packb(a); msg_ = msgpack.unpackb(msg)'
    total_time = timeit.timeit(test_code, setup=setup, number=count)
    print "total:",total_time
    print "r/s:", count/total_time


if __name__ == '__main__':
    set_a()
    test_get()
#    test_json_vs_msgpack()
