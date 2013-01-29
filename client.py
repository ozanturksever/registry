#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#

import sys
import time
from src.registry_client import RegistryClient

if __name__ == '__main__':
    def refresh():
        print 'callback:',c._RegistryClient__registry.get_values()

    c = RegistryClient(update_period=1, refresh_callback=refresh)
    if sys.argv[1] == 'set':
        c.set(sys.argv[2], sys.argv[3])
        c.commit()
    if sys.argv[1] == 'watch':
        while True:
            time.sleep(1)
