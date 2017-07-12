############################################
# Class Name CleanUpLoadConfig              #
# Synopsis: load yml config                 #
# +read_yalm_config_file(self,string):viod  #
# date       Change              who        #
# 2016-01-13 Created load conf   Abel Guzman#
############################################

import yaml


class CleanUpLoadConfig:
    def __init__(self):
        self.file = 'conf/conf.yml'

    def read_yalm_config_file(self, file_path=''):
        if (file_path != ''):
            self.file = file_path
        with open(self.file, 'r') as stream:
            doc_array = yaml.load(stream)
            return doc_array

# Class test
# print (CleanUpLoadConfig.read_yalm_config_file(CleanUpLoadConfig(),'/root/randy_collection/conf/conf.yml'))
