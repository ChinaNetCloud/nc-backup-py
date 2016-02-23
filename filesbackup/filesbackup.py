import argparse

class FileBackups:

    @staticmethod
    def files_backup():
        print "Executing files backup"

    def file_backup_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-i', '--FILESET_INCLUDE', type=str
                                   , help='Included fileset to backup', required=True)
        # args_list = parser_object.parse_args()
        args_list, unknown = parser_object.parse_known_args()
        return args_list


if __name__ == "__main__":
    FileBackups.files_backup()
    command_object = FileBackups.file_backup_commands(FileBackups())
    if command_object.FILESET_INCLUDE:
        print "Parameters in use: " + command_object.FILESET_INCLUDE