import argparse
import time
import os
import sys

class CompressionWorks:

    def __init__(self, tar_program='/usr/local/Cellar/gnu-tar/1.28/bin/tar czCf /', sudo_command='/usr/bin/sudo'):
        if tar_program=='' or tar_program is None:
            tar_program='/usr/local/Cellar/gnu-tar/1.28/bin/tar czCf /'
        if sudo_command=='' or sudo_command is None:
            sudo_command='/usr/bin/sudo'
        self.__tar_program = tar_program
        self.__sudo_command = sudo_command

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
        parser_object.add_argument('-C', '--COMPRESSION_CMD_CHAIN', type=str
                                   , help='This is the compression command software and it''s parameters',
                                   required=False)
        parser_object.add_argument('-s', '--SUDO_COMMAND', type=str
                               , help='Sudo command',
                               required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def compression_execution(self, objectives,destination):
        """Execute compression of files"""
        if objectives != '' and objectives is not None:
            objectives = objectives.replace(' /', ' ')
            objectives = objectives[1:]
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        # tar_command = '/usr/bin/sudo /bin/tar czCf / ' + destination + '/filesbackup_' \
        #                   + datetime_string + '.tar.gz ' + objectives
        tar_command = self.__sudo_command + ' ' + self.__tar_program + ' ' + destination + '/filesbackup_' \
                          + datetime_string + '.tar.gz ' + objectives
        if not os.path.isdir(destination):
            execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + destination)
            # SubprocessExecution.print_output(SubprocessExecution(), execution_mkdir)
        try:
            execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), tar_command)
            # SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        except Exception as e:
            e.args += (execution_message,)
            raise

if __name__ == "__main__":
    command_compression = CompressionWorks.compression_commands(CompressionWorks())
    if command_compression.OBJECTIVES and command_compression.DESTINATION:
        sys.path.append(command_compression.HOME_FOLDER)
        from execution.subprocess_execution import SubprocessExecution
        from tools.os_works import OSInformation
        from tools.filesystem_handling import FilesystemHandling

        print 'Files to compress: ' + command_compression.OBJECTIVES + '. This files will be compressed to: '\
              + command_compression.DESTINATION
        tar_execution = CompressionWorks.compression_execution(CompressionWorks(command_compression.COMPRESSION_CMD_CHAIN,
                                                                                command_compression.SUDO_COMMAND), command_compression.OBJECTIVES
                                                               , command_compression.DESTINATION)
    if command_compression.REMOVE_OBJECTIVES:
        print 'Deleting files after objective files as per config option --REMOVE_OBJECTIVES: ' \
              + command_compression.OBJECTIVES
        FilesystemHandling.remove_files(command_compression.OBJECTIVES)

