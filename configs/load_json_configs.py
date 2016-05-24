import json
import logging
import os.path


from collections import OrderedDict

class LoadJsonConfig:
    __config_file = '../conf/conf.json'

    def read_config_file(self, file_path=''):
        if file_path != '':
            self.__config_file = file_path
        if os.path.isfile(self.__config_file):
            try:
                with open(self.__config_file, 'r') as stream_doc:
		    print self.__config_file
                    doc_dict = json.load(stream_doc, object_pairs_hook=OrderedDict)
                    return doc_dict
            except EnvironmentError as e:
                logging.critical('Config json file found, but there was an error loading it: ',e.message)

        else:
            return 'File not found at ' + file_path
