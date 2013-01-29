#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import time
from src.registry_client import RegistryClient
from src.registry_server import RegistryServer

class TestIntegration:
    def test_set(self):
        server = RegistryServer(server_uri='tcp://127.0.0.1:11999')
        client = RegistryClient(server_uri='tcp://127.0.0.1:11999')
        client.set('a','b')
        client.set('x.y','z')
        client.commit()
        assert client._RegistryClient__registry.get_values() == server.get_values()
        client.set('a','c')
        assert client._RegistryClient__registry.get_values() != server.get_values()
