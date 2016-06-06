from subprocess import Popen
from subprocess import PIPE

# from subprocess import check_output
from subprocess import call
from subprocess import CalledProcessError
# from threading import Thread
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

        self.__process = Popen(shell_command, shell=True, stdout=PIPE, stderr=PIPE)
        if wait_cmd is True:
            self.__process.wait()
        #     if self.__process.poll() is None:
        return_code = self.__process.poll()
        stdout, stderr = self.__process.communicate()
        return return_code, stdout, 'stderr: ' + stderr

    def print_output(self, communicates_message):
        for message in communicates_message:
             if message != '':
                 print message


