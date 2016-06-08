import time


from tools.sample_module import ModuleFrame
from execution.config_parser import ConfigParser
from execution.subprocess_execution import SubprocessExecution

class MongoBackup(ModuleFrame):
    def __init__(self, parameters=None, logger=None):
        self.__parameters_dict = parameters
        self.__logger = logger

    def works_execution(self):
        # print self.__parameters_dict
        dir_mongo_backup = self.__parameters_dict['DESTINATION'] + '/' + self.__parameters_dict['PREFIX_FOLDER']
        print dir_mongo_backup
        if not ConfigParser.is_existing_abs_path(ConfigParser(), dir_mongo_backup):
            result_mkdir_mongo_backup = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    'mkdir ' + dir_mongo_backup,
                                                                                    self.__logger)
            if result_mkdir_mongo_backup[0] is not None and result_mkdir_mongo_backup[0] != 0:
                message_mkdir = 'Could not create direstory ' + dir_mongo_backup \
                                + ' if the software can not create mongo backup FAILS'
                self.__logger.critical(message_mkdir)
                print message_mkdir
                return 1, '', message_mkdir
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        if not ConfigParser.is_existing_abs_path(ConfigParser(), dir_mongo_backup + '/dump_' + datetime_string):
            result_mkdir_mongo_backup = ''
            result_mkdir_mongo_backup = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    'mkdir ' + dir_mongo_backup
                                                                                    + '/dump_' + datetime_string,
                                                                                    self.__logger)
            print result_mkdir_mongo_backup
            print type(result_mkdir_mongo_backup[0])
            print type(None)
            if result_mkdir_mongo_backup[0] is not None and result_mkdir_mongo_backup[0] != 0:
                message_mkdir = 'Could not create direstory ' + dir_mongo_backup + '/dump_' + datetime_string \
                                + ' if the software can not create this folder mongo backup FAILS'
                self.__logger.critical(message_mkdir)
                print message_mkdir
                return 1, '', message_mkdir
            print result_mkdir_mongo_backup
        mongo_dump_command = '$((mongodump -h 127.0.0.1 -o ' + dir_mongo_backup + '/dump_' + datetime_string + ') 1>/dev/null) 2>&1'
        result_mongo_dump_execution = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    mongo_dump_command,
                                                                                    self.__logger)

        print result_mongo_dump_execution
        # dir_mongo_backup = dir_mongo_backup[1:]
        compress_mongo_files_dir = self.__parameters_dict['TAR_COMMAND'] + ' ' + dir_mongo_backup + '/dump_' \
                                   + datetime_string + ".tar.gz" + ' ' + dir_mongo_backup + '/dump_' \
                                   + datetime_string
        print compress_mongo_files_dir
        result_compress_mongo_files_dir = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                       compress_mongo_files_dir,
                                                                                  self.__logger)
        print result_compress_mongo_files_dir


        result_remove_mongo_backup = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                        'rm  -rf ' + dir_mongo_backup + '/dump_' \
                                                                        + datetime_string,
                                                                        self.__logger)
        print result_remove_mongo_backup
        return result_remove_mongo_backup

