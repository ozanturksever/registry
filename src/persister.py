#
# Copyright (c) Innotim Yazilim Telekomunikasyon ve Danismanlik Ticaret LTD. STI.
# All rights reserved.
#
import copy
import json
from src.registry import Registry

class Persister(object):
    def __init__(self, load_files=[], output_file=None):
        self.__registry = Registry()
        self.load_files = load_files
        self.output_file = output_file
        for file in self.load_files:
            self.load_file(file)

    def load_file(self, file_path):
        try:
            f = open(file_path)
            json_content = f.read()
            f.close()
            data = json.loads(json_content)
            self.__registry.merge(data)
        except Exception, err:
#            print err
            pass

    def export(self, export_file_path=None):
        if not export_file_path:
            export_file_path = self.output_file
        f = open(export_file_path,'w')
        content = json.dumps(self.__registry.get_values()[1], indent=4)
        f.write(content)
        f.close()

    def set_registry_values(self, values):
        self.__registry.set_values(values)

    def get_values(self):
        return self.__registry.get_values()

