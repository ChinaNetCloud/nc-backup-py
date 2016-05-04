import argparse
import os
import time
import sys


class FileBackups:

    def __init__(self, tar_program='/usr/local/Cellar/gnu-tar/1.28/bin/tar czCf /', sudo_command='/usr/bin/sudo'):
        if tar_program=='' or tar_program is None:
            tar_program='/usr/local/Cellar/gnu-tar/1.28/bin/tar czCf /'
        if sudo_command=='' or sudo_command is None:
            sudo_command='/usr/bin/sudo'
        self.__tar_program = tar_program
        self.__sudo_command = sudo_command

    @staticmethod
    def files_backup():
        print "Executing files backup"

    def file_backup_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-i', '--FILESET_INCLUDE', type=str
                                   , help='Included fileset to backup', required=True)
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str
                                   , help='Script home folder required(from where the master script runs)', required=True)
        parser_object.add_argument('-w', '--WORK_FOLDER', type=str
                                   , help='This is the folder to use for temporary files works', required=True)
        parser_object.add_argument('-C', '--COMPRESSION_CMD_CHAIN', type=str
                                   , help='This is the compression command software and it''s parameters', required=False)
        parser_object.add_argument('-s', '--SUDO_COMMAND', type=str
                                   , help='Sudo command',
                                   required=False)
        parser_object.add_argument('-e', '--FILESET_EXCLUDE', type=str
                                   , help='Files not to be included', required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def file_backup_execution(self, filesets, destination='', excluded_filesets=''):
        """Execute the files tar and compression"""
        # #Files and folders checkups
        # Included filesets
        print 'Making a compressed copy of the local files to: ' + destination
        if filesets != '' and filesets is not None:
            filesets = filesets.replace(' /', ' ')
            filesets = filesets[1:]
        else:
            print
            sys.stderr.write('ERROR: The --FILESET_INCLUDE can not be empty; execution')
            sys.exit(1)
        if excluded_filesets:
            print 'Backup objective(s): ' + filesets + '. Excluded files: ' + excluded_filesets
        else:
            print 'Backup objective(s): ' + filesets + '. No files Excluded.'
        # Excluded filesets
        if excluded_filesets != '' and excluded_filesets is not None:
            excluded_files = ' --exclude=' + excluded_filesets[1:]
            excluded_files = excluded_files.replace('/ ', ' ')
            excluded_files = excluded_files.replace(' /', ' --exclude ')
        else:
            excluded_files = ''
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        os_name = OSInformation.isWindows()
        execution_message = 'Error'
        if (os_name):
            print 'Windows compression command here'

        else:
            if os.geteuid() == 0:
                sys.stderr.write('Execution as root is not allowed the GID for this user can not be 0')
                exit(1)
            else:
                tar_command = self.__sudo_command + ' ' + self.__tar_program + ' ' + destination + '/files/filesbackup_' \
                              + datetime_string + '.tar.gz ' + filesets + excluded_files
                # print tar_command
                if not os.path.isdir(destination + '/files'):
                    create_dir_cmd = 'mkdir ' + destination + '/files'
                    execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), create_dir_cmd)
                    if execution_mkdir != 0:
                        print 'Could Not create directory with command: ' + create_dir_cmd
                        print 'Error code: ' + str(execution_mkdir)
            try:
                execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), tar_command, True)
                # SubprocessExecution.print_output(SubprocessExecution(), execution_message)
            except Exception as e:
                e.args += (execution_message,)
                raise
            if execution_message != 0:
                print 'Executing the tar command: ' + tar_command
                print 'Returned nor zero exit code: ' + str(execution_message)


if __name__ == "__main__":
    FileBackups.files_backup()
    command_object = FileBackups.file_backup_commands(FileBackups())
    if command_object.FILESET_INCLUDE:
        sys.path.append(command_object.HOME_FOLDER)
        from execution.subprocess_execution import SubprocessExecution
        from tools.os_works import OSInformation
        print "Parameters in use, Fileset: " + command_object.FILESET_INCLUDE
        print 'Work Folder: ' + command_object.WORK_FOLDER
        print 'Files and folders to exclude:' + command_object.FILESET_EXCLUDE

        tar_execution = FileBackups.file_backup_execution(FileBackups(command_object.COMPRESSION_CMD_CHAIN
                                                                      , command_object.SUDO_COMMAND)
                                                          , command_object.FILESET_INCLUDE
                                                          , command_object.WORK_FOLDER, command_object.FILESET_EXCLUDE)
