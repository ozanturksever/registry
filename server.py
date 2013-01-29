#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import time
from src.persister import Persister
from src.registry_server import RegistryServer

CONFIG_FILE = 'defaults.cfg'

if __name__ == "__main__":
    persister = Persister([CONFIG_FILE], output_file=CONFIG_FILE)
    def refresh(registry_server):
        persister.set_registry_values(registry_server.get_values()[1])
        persister.export()

    registry_server = RegistryServer(initial_value=persister.get_values()[1], refresh_callback=refresh)
    while True:
        time.sleep(1)