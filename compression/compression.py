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
        parser_object.add_argument('-o', '--OBJECTIVES', '--TARGETS', type=str
                                   , help='Included fileset to compress', required=False)
        parser_object.add_argument('-d', '--DESTINATION', type=str
                                   , help='Compress files to folder', required=False)
        parser_object.add_argument('-r', '--REMOVE_OBJECTIVES', '--REMOVE_TARGETS', type=str
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

    @staticmethod
    def check_exists(self, variable_to_check):
        if not variable_to_check or \
                        variable_to_check is None or \
                        variable_to_check == '':
            return False
        return True

    def get_immediate_subdirectories(self, a_dir):
        return [a_dir + '/' + name for name in os.listdir(a_dir)
                if os.path.isdir(os.path.join(a_dir, name))]

if __name__ == "__main__":
    command_compression = CompressionWorks.compression_commands(CompressionWorks())
    if not CompressionWorks.check_exists(CompressionWorks(),command_compression.TAR_COMMAND):
        command_compression.TAR_COMMAND = 'sudo /bin/tar czCf /'
    if not CompressionWorks.check_exists(CompressionWorks(),command_compression.DESTINATION):
        command_compression.DESTINATION = '/opt/backup/compressed'
    if not CompressionWorks.check_exists(CompressionWorks(),command_compression.REMOVE_OBJECTIVES):
        command_compression.REMOVE_OBJECTIVES = 'True'
    if not CompressionWorks.check_exists(CompressionWorks(),command_compression.OBJECTIVES):
        objectives_names_list = CompressionWorks.get_immediate_subdirectories(CompressionWorks(), '/opt/backup')
        command_compression.OBJECTIVES = ''
        for objectives_name in objectives_names_list:
            if command_compression.OBJECTIVES == '':
                command_compression.OBJECTIVES += objectives_name
            else:
                command_compression.OBJECTIVES += ' ' + objectives_name

    # print command_compression.OBJECTIVES
    # exit(1)
    if command_compression.OBJECTIVES:
        sys.path.append(command_compression.HOME_FOLDER)
        from execution.subprocess_execution import SubprocessExecution
        from tools.filesystem_handling import FilesystemHandling
        from execution.config_parser import ConfigParser

        execute = False
        for objectives_paths in str(command_compression.OBJECTIVES).split():
            if not ConfigParser.is_existing_abs_path(ConfigParser(), objectives_paths):
                execute = False
                break
            execute = True

            tar_execution = CompressionWorks.compression_execution(CompressionWorks(command_compression.TAR_COMMAND),
                                                                   command_compression.OBJECTIVES,
                                                                   command_compression.DESTINATION)
            print tar_execution

    else:
        print 'OBJECTIVES and DESTINATION need to be present in compression module, execution will not continue'
        exit(1)

    if command_compression.REMOVE_OBJECTIVES == True or command_compression.REMOVE_OBJECTIVES == 'True':
        print 'Deleting files after objective files as per config option --REMOVE_OBJECTIVES: ' \
              + command_compression.OBJECTIVES
        FilesystemHandling.remove_files(command_compression.OBJECTIVES)

