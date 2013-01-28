#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
from src.registry_client import RegistryClient

class TestIntegration:
    def test_set(self):
        c = RegistryClient()
#        c.set('xx','xxyy')
#        c.commit()
        print c._RegistryClient__registry.get_values()
