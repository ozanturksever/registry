#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from src.interfaces.registry_server import IRegistryServer
from src.msg_thread import MsgThread
from src.registry import Registry
from src.server_socket import ServerSocket

SERVER_URI = 'tcp://127.0.0.1:10000'

class RegistryServer(object, IRegistryServer):
    def __init__(self, initial_value = {}):
        self.__registry = Registry(initial_value)
        self.socket = ServerSocket(SERVER_URI)
        self._start_msg_thread()

    def _start_msg_thread(self):
        self.msg_thread = MsgThread(self, self.socket)
        self.msg_thread.daemon = True
        self.msg_thread.start()

    def _stop_msg_thread(self):
        self.msg_thread.exit()

    def get(self, key):
        return self.__registry.get(key)

    def set(self, key, value):
        return self.__registry.set(key,value)

    def commit(self, values):
        self.__registry.set_values(values)

    def get_values(self):
        return self.__registry.get_values()

    def get_version(self):
        return self.__registry.get_version()
