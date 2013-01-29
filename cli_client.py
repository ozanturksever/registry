#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import json
import pprint

import sys
import time
from src.registry_client import RegistryClient

if __name__ == '__main__':
    def refresh(registry_client):
        print "---"
        pprint.pprint(registry_client.get_values())
        print ""

    c = RegistryClient(update_period=1, refresh_callback=refresh)
    if sys.argv[1] == 'set':
        c.set(sys.argv[2], sys.argv[3])
        c.commit()
    if sys.argv[1] == 'set_json':
        c.set(sys.argv[2], json.loads(sys.argv[3]))
        c.commit()
    if sys.argv[1] == 'remove':
        c.remove(sys.argv[2])
        c.commit()
    if sys.argv[1] == 'watch':
        while True:
            time.sleep(1)
