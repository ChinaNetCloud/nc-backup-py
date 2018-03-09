from Queue import Queue, Empty

try:
    from subprocess import check_output, CalledProcessError
except ImportError:
    print "Unable to import subprocess.check_output, are you using python 2.6?"
    print "Using self defined check_output."

    import subprocess_patch

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

        return return_code, stdout, 'stderr: ' + stderr

    def print_output(self, communicates_message):
        for message in communicates_message:
            if message != '':
                print message
