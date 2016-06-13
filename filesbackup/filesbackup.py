import argparse
import os
import time
import sys


class FileBackups:

    def file_backup_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-i', '--FILESET_INCLUDE', type=str
                                   , help='Included fileset to backup', required=True)
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str,
                                   help='Script home folder required(from where the master script runs)',
                                   required=True)
        parser_object.add_argument('-w', '--WORK_FOLDER', type=str
                                   , help='This is the folder to use for temporary files works', required=True)
        parser_object.add_argument('-C', '--COMPRESSION_CMD_CHAIN', type=str
                                   , help='This is the compression command software and it''s parameters', required=False)
        parser_object.add_argument('-T', '--TAR_COMMAND', type=str
                                   , help='Tar command',
                                   required=False)
        parser_object.add_argument('-e', '--FILESET_EXCLUDE', type=str
                                   , help='Files not to be included', required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def file_backup_execution(self, filesets, destination='', excluded_filesets='', tar_command=''):
        """Execute the files tar and compression"""
        print 'Making a compressed copy of the local files to: ' + destination
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
            if not os.path.isdir(destination + '\\files'):
                create_dir_cmd = 'mkdir ' + destination + '\\files'
                execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), create_dir_cmd, True)
                print execution_mkdir
            result_file_name = destination + '\\files\\compressed\\filebackup_' + datetime_string
            filesets = filesets.split()
            ZipCompression(result_file_name + '.zip', filesets)

        else:
            if filesets != '' and filesets is not None:
                filesets = filesets.replace(' /', ' ')
                filesets = filesets[1:]
            else:
                print
                sys.stderr.write('ERROR: The --FILESET_INCLUDE can not be empty; execution')
                sys.exit(1)
            if os.geteuid() == 0:
                sys.stderr.write('Execution as root is not allowed the GID for this user can not be 0')
                exit(1)
            else:
                tar_command = tar_command + ' ' + destination + '/files/filesbackup_' \
                              + datetime_string + '.tar.gz ' + filesets + excluded_files
                if not os.path.isdir(destination + '/files'):
                    create_dir_cmd = 'mkdir ' + destination + '/files'
                    execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), create_dir_cmd, True)
                    if execution_mkdir[0] != 0:
                        print 'Could Not create directory with command: ' + create_dir_cmd
                        print 'Error code: ' + str(execution_mkdir[0])
            execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), tar_command, True)
            print execution_message
            if execution_message [0] != 0:
                print 'Executing the tar command: ' + tar_command
                print 'Returned nor zero exit code: ' + str(execution_message[0],) + ', ' + str(execution_message[1]) + \
                      ', ' + str(execution_message[2])
                exit(1)
            else:
                print 'Successful execution: ' + str(execution_message[0]) + ', ' + str(execution_message[1]) + \
                      ', ' + str(execution_message[2])

    def evaluate_file_or_folder(self, paths_string):
        """
        @rtype: bool
        """

        # print paths_string
        for path_string in paths_string.split():
            if not ConfigParser.is_existing_abs_path(ConfigParser(), path_string):
                return False
        return True

if __name__ == "__main__":
    command_object = FileBackups.file_backup_commands(FileBackups())
    if command_object.FILESET_INCLUDE:
        sys.path.append(command_object.HOME_FOLDER)
        from compression.zip_compression import ZipCompression
        from execution.subprocess_execution import SubprocessExecution
        from tools.os_works import OSInformation
        from execution.config_parser import ConfigParser
        if not FileBackups.evaluate_file_or_folder(FileBackups(), command_object.FILESET_INCLUDE):
            print "At least one of the filesets (FILESET_INCLUDE variable from configs)" \
                  " for files backup does not exist this script is terminating"
            exit(1)
        # print command_object.FILESET_EXCLUDE
        if command_object.FILESET_EXCLUDE and not FileBackups.evaluate_file_or_folder(FileBackups(), command_object.FILESET_EXCLUDE):
            print "At least one of the Excluded filesets (FILESET_EXCLUDE variable from configs) " \
                  "for files backup does not exist this script is terminating"
            exit(1)
        print "Parameters in use, Fileset: " + command_object.FILESET_INCLUDE
        print 'Work Folder: ' + command_object.WORK_FOLDER
        print 'Files and folders to exclude:' + str(command_object.FILESET_EXCLUDE)
        if command_object.TAR_COMMAND:
            tar_command = command_object.TAR_COMMAND
        else:
            tar_command = 'sudo /bin/tar czCf /'
        FileBackups.file_backup_execution(FileBackups(),
                                          command_object.FILESET_INCLUDE,
                                          command_object.WORK_FOLDER,
                                          command_object.FILESET_EXCLUDE, tar_command)
