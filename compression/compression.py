import argparse
import time
import os
import sys

class CompressionWorks:

    def __init__(self, tar_program=''):
        if tar_program=='' or tar_program is None:
            tar_program=''
        self.__tar_program = tar_program

    def compression_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', type=str
                                   , help='Included fileset to compress', required=True)
        parser_object.add_argument('-d', '--DESTINATION', type=str
                                   , help='Compress files to folder', required=True)
        parser_object.add_argument('-r', '--REMOVE_OBJECTIVES', type=str
                                   , help='Remove/Delete objective folders', required=False)
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str
                                   , help='home folder for the modules to include', required=True)
        parser_object.add_argument('-s', '--TAR_COMMAND', type=str
                               , help='tar command',
                               required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def compression_execution(self, objectives,destination):
        """Execute compression of files"""
        objectives_list = objectives.split()
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        # print objectives_list
        tar_command = self.__tar_program + ' ' + destination + '/filesbackup_' \
        + datetime_string + '.tar.gz '
        for objective in objectives_list:
            if objective != '' and objective is not None:
                objective = objective.replace(' /', ' ')
                objective = objective[1:]
                tar_command = tar_command + ' ' + objective
                if not os.path.isdir(destination):
                    execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + destination)

        print tar_command
        execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), tar_command)

        return execution_message

if __name__ == "__main__":
    command_compression = CompressionWorks.compression_commands(CompressionWorks())
    if command_compression.OBJECTIVES and command_compression.DESTINATION:
        sys.path.append(command_compression.HOME_FOLDER)
        from execution.subprocess_execution import SubprocessExecution
        # from tools.os_works import OSInformation
        from tools.filesystem_handling import FilesystemHandling
        from execution.config_parser import ConfigParser

        print command_compression.OBJECTIVES
        # print ConfigParser.is_existing_abs_path(ConfigParser(), command_compression.OBJECTIVES)
        # print ConfigParser.is_abs_path(ConfigParser(), command_compression.DESTINATION)
        execute = False
        for objectives_paths in str(command_compression.OBJECTIVES).split():
            if not ConfigParser.is_existing_abs_path(ConfigParser(), objectives_paths):
                execute = False
                break
            execute = True
        if execute and ConfigParser.is_abs_path(ConfigParser(), command_compression.DESTINATION):
            print 'Files to compress: ' + command_compression.OBJECTIVES + '. This files will be compressed to: '\
                  + command_compression.DESTINATION
            tar_execution = CompressionWorks.compression_execution(CompressionWorks(command_compression.TAR_COMMAND),
                                                                   command_compression.OBJECTIVES,
                                                                   command_compression.DESTINATION)
            print tar_execution
        else:
            print 'Please make sure OBJECTIVES exist and DESTINATION is absolute path, execution will not continue'
            exit(1)
    else:
        print 'OBJECTIVES and DESTINATION need to be present in compression module, execution will not continue'
        exit(1)

    if command_compression.REMOVE_OBJECTIVES == True or command_compression.REMOVE_OBJECTIVES == 'True':
        print 'Deleting files after objective files as per config option --REMOVE_OBJECTIVES: ' \
              + command_compression.OBJECTIVES
        FilesystemHandling.remove_files(command_compression.OBJECTIVES)

