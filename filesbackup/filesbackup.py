import argparse
import os
import time
import subprocess
import sys

from execution.subprocess_execution import SubprocessExecution


class FileBackups:
    @staticmethod
    def files_backup():
        print "Executing files backup"

    def file_backup_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-i', '--FILESET_INCLUDE', type=str
                                   , help='Included fileset to backup', required=True)
        parser_object.add_argument('-w', '--WORK_FOLDER', type=str
                                   , help='This is the folder to use for temporary files works', required=True)
        parser_object.add_argument('-e', '--FILESET_EXCLUDE', type=str
                                   , help='files not to be included', required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def file_backup_execution(self, filesets, destination='', excluded_filesets=''):
        """Execute the files tar and compression"""
        # #Files and folders checkups
        # Included filesets
        print 'Making temporary copy of the local files to backup in: ' + destination
        if filesets != '' and filesets is not None:
            filesets = filesets.replace(' /', ' ')
            filesets = filesets[1:]
        else:
            print
            sys.stderr.write('ERROR: The --FILESET_INCLUDE can not be empty; execution')
            sys.exit(1)

        print 'Backup objective(s): ' + filesets + '. Excluded files: ' + excluded_filesets
        # Excluded filesets
        if excluded_filesets != '' and excluded_filesets is not None:
            excluded_files = ' --exclude=' + excluded_filesets[1:]
            excluded_files = excluded_files.replace('/ ', ' ')
            excluded_files = excluded_files.replace(' /', ' --exclude=')

        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        if os.geteuid() == 0:
            sys.stderr.write('Execution as root is not allowed the GID for this user can not be 0')
            exit(1)
        else:
            tar_command = '/usr/bin/sudo /bin/tar czCf / ' + destination + '/filesbackup_' + datetime_string + 'tar.gz ' \
                          + filesets + excluded_files
            print 'Command to execute: ' + tar_command
            try:
                # tar_result = commands.getstatusoutput(a)
                tar_result = subprocess.Popen(tar_command, shell=True, stdout=subprocess.PIPE,
                                              stderr=subprocess.PIPE)
                return tar_result
            except Exception as e:
                e.args += (tar_result,)
                raise


if __name__ == "__main__":
    FileBackups.files_backup()
    command_object = FileBackups.file_backup_commands(FileBackups())
    if command_object.FILESET_INCLUDE:
        print "Parameters in use, Fileset: " + command_object.FILESET_INCLUDE \
              + ', Work Folder: ' + command_object.WORK_FOLDER
        tar_execution = FileBackups.file_backup_execution(FileBackups(), command_object.FILESET_INCLUDE
                                                          , command_object.WORK_FOLDER, command_object.FILESET_EXCLUDE)
        print tar_execution
