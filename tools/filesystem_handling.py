from os.path import isdir

from execution.subprocess_execution import SubprocessExecution


class FilesystemHandling:

    @staticmethod
    def create_directory(destination):
        if not isdir(destination):
            execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + destination)
            SubprocessExecution.print_output(SubprocessExecution(), execution_mkdir)

    @staticmethod
    def remove_files(remove_objectives):
        try:
            delete_command = 'rm -rf ' + remove_objectives
            execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), delete_command)
            SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        except Exception as e:
            e.args += (execution_message,)
            raise