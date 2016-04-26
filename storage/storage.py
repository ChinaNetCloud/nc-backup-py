import argparse
import sys


class StorageExecution:

    def storage_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', type=str
                                   , help='Objectives to encrypt', required=True)
        parser_object.add_argument('-l', '--LOCAL_BACKUP', type=str
                                   , help='Objectives to encrypt', required=True)
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str
                                   , help='Path to the whole project folder, '
                                          'to include other libruaries', required=True)
        parser_object.add_argument('-D', '--DESTINATION', type=str
                                   , help='Backup destination', required=True)
        args_list, unknown = parser_object.parse_known_args()
        return args_list


if __name__ == "__main__":
    storage_cmd = StorageExecution.storage_commands(StorageExecution())
    if storage_cmd.DESTINATION == 'local':
        sys.path.append(storage_cmd.HOME_FOLDER)
        from tools.filesystem_handling import FilesystemHandling
        from execution.subprocess_execution import SubprocessExecution
        print 'Executing backup files type: ' + storage_cmd.DESTINATION
        command_move = 'mv ' + storage_cmd.OBJECTIVES + '/* ' + storage_cmd.LOCAL_BACKUP
        FilesystemHandling.create_directory(storage_cmd.LOCAL_BACKUP)
        ExecuteBackup = SubprocessExecution.main_execution_function(SubprocessExecution(), command_move, True)
        SubprocessExecution.print_output(SubprocessExecution(), ExecuteBackup)
        FilesystemHandling.remove_files(storage_cmd.OBJECTIVES)

