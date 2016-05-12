import os


class SizeCalculation:
    def __init__(self, parameters):
         self.__parameters_dict = parameters
         # print self.__parameters_dict['OBJECTIVES']
    def config_plugin(self):
        print 'Size calculation plugin\'s config is NOT in use'

    def works_execution(self):
        return self.get_dir_size(self.__parameters_dict['OBJECTIVES'])

    def output(self):
        return str("{0:.2f}".format(self.__size_final/1024.00/1024.00))+'M'

    def get_dir_size(self, directory_objective):
        size = 0
        for path, dirs, files in os.walk(directory_objective):
            for f in files:
                size += os.path.getsize(os.path.join(path, f))
        self.__size_final = size
        return 'Size calculation Done for ' + directory_objective +', get results from output'