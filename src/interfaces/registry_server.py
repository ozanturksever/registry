#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#

class IRegistryServer:
    def get(self, key):
        """get"""

    def set(self, key, value):
        """set"""

    def commit(self, values):
        """commit"""

    def get_values(self):
        """get_values"""

    def get_version(self):
        """"get_version"""