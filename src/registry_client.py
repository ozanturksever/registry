#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import time
from threading import Thread
from registry import Registry
from socket import Socket
from src.interfaces.registry_client import IRegistryClient

SERVER_URI = 'tcp://127.0.0.1:10000'

try:
    import msgpack
except ImportError:
    import msgpack_pure as msgpack

class UpdateThread(Thread):
    _exit = False

    def __init__(self, registry, update_period):
        if not isinstance(registry, IRegistryClient):
            raise Exception("registry must be IRegistryClient instance")

        self.registry = registry
        self.update_period = update_period

        Thread.__init__(self)

    def run(self):
        time.sleep(self.update_period)
        while not self._exit:
            self.registry.refresh()
            time.sleep(self.update_period)

    def exit(self):
        self._exit = True

class RegistryClient(object, IRegistryClient):
    def __init__(self, update_period=10, refresh_callback=None):
        self.__cached_values = {}
        self.__refresh_callback = refresh_callback
        self.__update_period = update_period
        self.__socket = Socket(SERVER_URI)
        self.__registry = Registry()
        self._load()
        self.__update_thread = UpdateThread(self, update_period)
        self.__update_thread.daemon = True
        self.__update_thread.start()

    def get(self, key):
        return self.__registry.get(key)

    def set(self, key, value):
        return self.__registry.set(key, value)

    def refresh(self):
        current_version = self.__socket.send('get_version')
        if self.__registry.get_version() != current_version:
            self._load()
            if self.__refresh_callback:
                self.__refresh_callback()

    def _load(self):
        try:
            (version,values) = self.__socket.send('get_values')
            if values:
                self.__registry.set_values(values, version)
        except Exception, err:
            print "Ops:",err
            pass

    def commit(self):
        server_version = self.__socket.send('commit', self.__registry.get_values()[1])
        self.__registry.update_version(server_version)