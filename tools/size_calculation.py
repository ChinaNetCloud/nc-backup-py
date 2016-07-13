import os


from os_works import OSInformation
from execution.config_parser import ConfigParser

class SizeCalculation:
    def __init__(self, parameters, logger=None):
         self.__parameters_dict = parameters
         self.__logger = logger
    def config_plugin(self):
        pass

    def works_execution(self):
        return self.get_dir_size(self.__parameters_dict['OBJECTIVES'])

    def output(self):
        return OSInformation.human_readable_size(self.__size_final)

    def get_dir_size(self, directory_objective):
        size = 0
        if not ConfigParser.is_existing_abs_path(ConfigParser(), directory_objective):
            size_path_error = 'The path provided to calculate size does not exist.'
            self.__logger.warning(size_path_error)
            return size_path_error

        for path, dirs, files in os.walk(directory_objective):
            for f in files:
                size += os.path.getsize(os.path.join(path, f))
        self.__size_final = size
        return 'Size calculation Done for ' + directory_objective +', get results from output'

