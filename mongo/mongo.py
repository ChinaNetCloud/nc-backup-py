import time


from tools.sample_module import ModuleFrame
from execution.config_parser import ConfigParser
from execution.subprocess_execution import SubprocessExecution

class MongoBackup(ModuleFrame):
    def __init__(self, parameters=None, logger=None):
        self.__parameters_dict = parameters
        self.__logger = logger

    def output(self):
        return self.__result_mongo_dump_execution

    def works_execution(self):
        # VALIDATIONS PENDING
        if not self.__parameters_dict['DESTINATION'] \
                or not ConfigParser.is_existing_abs_path(ConfigParser(), self.__parameters_dict['DESTINATION']):
            destination_not_found = 'Mongo script needs a DESTINATION folder: ' \
                  + self.__parameters_dict['DESTINATION'] + ' can not be found.'
            print destination_not_found
            self.__logger(destination_not_found)
            return 1, '', destination_not_found
        dir_mongo_backup = self.__parameters_dict['DESTINATION'] + '/' + self.__parameters_dict['PREFIX_FOLDER']
        if not ConfigParser.is_existing_abs_path(ConfigParser(), dir_mongo_backup):
            result_mkdir_mongo_backup = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    'mkdir ' + dir_mongo_backup,
                                                                                    self.__logger)
            self.__logger.info(result_mkdir_mongo_backup)
            if result_mkdir_mongo_backup[0] is not None and result_mkdir_mongo_backup[0] != 0:
                message_mkdir = 'Could not create direstory ' + dir_mongo_backup \
                                + ' if the software can not create mongo backup FAILS'
                self.__logger.critical(message_mkdir)
                print message_mkdir
                self.__result_mongo_dump_execution = 1, '', message_mkdir
                return 1, '', message_mkdir
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        if not ConfigParser.is_existing_abs_path(ConfigParser(), dir_mongo_backup + '/dump_' + datetime_string):
            result_mkdir_mongo_backup = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    'mkdir ' + dir_mongo_backup
                                                                                    + '/dump_' + datetime_string,
                                                                                    self.__logger)
            self.__logger.info(result_mkdir_mongo_backup)
            if result_mkdir_mongo_backup[0] is not None and result_mkdir_mongo_backup[0] != 0:
                message_mkdir = 'Could not create direstory ' + dir_mongo_backup + '/dump_' + datetime_string \
                                + ' if the software can not create this folder mongo backup FAILS'
                self.__logger.critical(message_mkdir)
                print message_mkdir
                self.__result_mongo_dump_execution = 1, '', message_mkdir
                return 1, '', message_mkdir
            print result_mkdir_mongo_backup
        mongo_dump_command = self.__parameters_dict['MONGODUMP_BIN']
        if type(self.__parameters_dict['MONGO_HOST']) is str:
            mongo_host = self.__parameters_dict['MONGO_HOST']
        else:
            mongo_host = '127.0.0.1'
        mongo_dump_command += ' -h ' + mongo_host + ' -o ' + dir_mongo_backup + '/dump_' + datetime_string
        if self.__parameters_dict['MONGO_USER'] != '' and self.__parameters_dict['MONGO_USER'] is not None:
            mongo_dump_command += ' --username ' + self.__parameters_dict['MONGO_USER']
        if self.__parameters_dict['MONGO_PWD'] != '' and self.__parameters_dict['MONGO_PWD'] is not None:
            mongo_dump_command += ' --password ' + self.__parameters_dict['MONGO_PWD']
        result_mongo_dump_execution = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    mongo_dump_command,
                                                                                    True, self.__logger)
        # print result_mongo_dump_execution
        if result_mongo_dump_execution[0] != 0 and result_mongo_dump_execution[0] is not None:
            self.__logger.warning('MongoDB backup failed')
            self.__logger.warning('Error code: ' + str(result_mongo_dump_execution[0]))
            self.__logger.warning('StdOut: ' + str(result_mongo_dump_execution[1]))
            self.__logger.warning(str(result_mongo_dump_execution[2]))
            self.__result_mongo_dump_execution = result_mongo_dump_execution
            return result_mongo_dump_execution

        compress_mongo_files_dir = self.__parameters_dict['TAR_COMMAND'] + ' ' + dir_mongo_backup + '/dump_' \
                                   + datetime_string + ".tar.gz" + ' ' + dir_mongo_backup + '/dump_' \
                                   + datetime_string
        SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                       compress_mongo_files_dir,
                                                                                  self.__logger)


        SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                        'rm  -rf ' + dir_mongo_backup + '/dump_' \
                                                                        + datetime_string,
                                                                        self.__logger)
        # print result_mongo_dump_execution
        self.__result_mongo_dump_execution = result_mongo_dump_execution
        return 'Execution finished successfully'

