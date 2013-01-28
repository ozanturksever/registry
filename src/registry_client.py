#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import copy
from registry import Registry
from socket import Socket

SERVER_URI = 'tcp://127.0.0.1:10000'

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack

class RegistryClient(object):
    def __init__(self):
        self.__cached_values = {}
        self.__socket = Socket(SERVER_URI)
        self.__registry = Registry()
        self._load()

    def get(self, key):
        return self.__registry.get(key)

    def set(self, key, value):
        return self.__registry.set(key, value)

    def _load(self):
        try:
            (version,values) = self.__socket.send('get_values')
            if values:
                self.__registry.set_values(values, version)
        except:
            pass

    def commit(self):
        server_version = self.__socket.send('commit', self.__registry.get_values()[1])
        self.__registry.update_version(server_version)