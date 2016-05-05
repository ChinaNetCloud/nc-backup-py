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

    def main_execution_function(self, shell_command, wait_cmd=True):
        """
        :rtype: stdout, stderr
        """
        log_string = 'Executing system the system external command: ' + shell_command
        print log_string
        # logger.info(log_string)
        # self.__process = Popen(shell_command, shell=True, stdout=PIPE, stderr=PIPE)
        try:
            self.__process = Popen(shell_command, shell=True, stdout=PIPE, stderr=PIPE)
        except CalledProcessError as e:
            return 1
        if wait_cmd is True:
            self.__process.wait()

        return_code = self.__process.poll()
        stdout, stderr = self.__process.communicate()
        # print stdout
        # print stderr
        return return_code, stdout, stderr
        # stdout, stderr = self.__process.communicate()
        # # print 'Error: ' + stderr
        # return stdout, stderr

    def print_output(self, communicates_message):
        for message in communicates_message:
             if message != '':
                 print message


