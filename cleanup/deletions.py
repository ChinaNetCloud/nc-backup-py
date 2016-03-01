from execution.subprocess_execution import SubprocessExecution


class DeleteFiles:
    """This class is to delete files"""
    def remove_files(self, remove_objectives):
        try:
            delete_command = 'rm -rf ' + remove_objectives
            execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), delete_command)
            SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        except Exception as e:
            e.args += (execution_message,)
            raise