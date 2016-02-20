import json
import os.path


from collections import OrderedDict

class LoadJsonConfig:
    __config_file = 'conf/conf.json'

    def read_config_file(self, file_path=''):
        if file_path != '':
            self.__config_file = file_path
        if os.path.isfile(self.__config_file):
            with open(self.__config_file, 'r') as stream_doc:
                doc_dict = json.load(stream_doc, object_pairs_hook=OrderedDict)
                return doc_dict
        else:
            return 'File not found at ' + file_path
