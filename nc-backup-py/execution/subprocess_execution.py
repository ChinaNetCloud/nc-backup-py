from subprocess import check_output
from subprocess import CalledProcessError
from Queue import Queue, Empty


class SubprocessExecution:
    __io_q = Queue()
    __process = None

    def main_execution_function(self, shell_command, wait_cmd=True, logger=None):
        """
        :rtype: stdout, stderr
        """
        log_string = 'Executing system the system external command: ' + shell_command
        if logger is not None:
            logger.info(log_string)
        else:
            print log_string

        return_code = 0
        stdout = stderr = ''
        try:
            stdout = check_output(shell_command, shell=True)
        except CalledProcessError as e:
            return_code = e.returncode
            stderr = e.output
        # Debug return codes

        # print("".center(79, '-'))
        # print("stdout: %s " % stdout)
        # print("type(stdout: %s " % type(stdout))
        # print("stderr: %s " % stderr)
        # print("type(stderr: %s " % type(stderr))
        # print("return_code: %s " % return_code )
        # print("type(return_code: %s " % type(return_code))
        # print("".center(79, '-'))

        return return_code, stdout, 'stderr: ' + stderr

    def print_output(self, communicates_message):
        for message in communicates_message:
             if message != '':
                 print message


