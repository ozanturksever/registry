#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import time
from src.registry_server import RegistryServer

if __name__ == "__main__":
    r = RegistryServer()
    while True:
        time.sleep(1)