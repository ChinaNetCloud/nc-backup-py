from os.path import isdir

from execution.subprocess_execution import SubprocessExecution


class FilesystemHandling:

    @staticmethod
    def create_directory(destination):
        if not isdir(destination):
            execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + destination)
            # SubprocessExecution.print_output(SubprocessExecution(), execution_mkdir)

    @staticmethod
    def remove_files(objectives):
        try:
            delete_command = 'rm -rf ' + objectives
            execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), delete_command)
            return SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        except Exception as e:
            e.args += (execution_message,)
            raise


def remove_objectives(objectives, remove_objectives):
    """Check if REMOVE_OBJECTIVES is True and call remove_files."""
    if remove_objectives in ['True', 'true', 'TRUE', True, None, '']:
        print('Config option --REMOVE_OBJECTIVES set to True ')
        print('Deleting files %s' % remove_objectives)
        print(FilesystemHandling.remove_files(objectives))
    else:
        print('REMOVE_TARGETS not set to True.')
