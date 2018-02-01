from execution.subprocess_execution import SubprocessExecution

class RsyncBackup:
    def __init__(self, parameters, logger=None):
        self.__parameters_dict = parameters
        self.__logger = logger


    def config_plugin(self):
        pass

    def works_execution(self):
        rsync_commands = self.iterate_works('ORIGIN_AND_TARGETS_PARAMS')
        for i in rsync_commands:
            execution_output = SubprocessExecution.main_execution_function(SubprocessExecution()
                                                                       , rsync_commands[i], True
                                                                       , self.__logger)
        return execution_output

    def output(self):
        pass

    def iterate_works(self, iterate_string = None):
        if iterate_string is not None or iterate_string is not '':
            iterate_dict = self.__parameters_dict[iterate_string]
        else:
            iterate_dict = self.__parameters_dict
        return iterate_dict
