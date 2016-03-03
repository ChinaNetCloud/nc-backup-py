from subprocess import Popen
from subprocess import PIPE
from threading import Thread
from Queue import Queue, Empty


class SubprocessExecution:
    __io_q = Queue()
    __process = None

    def main_execution_function(self, shell_command, wait_cmd=False):
        """

        :rtype: stdout, stderr
        """
        print 'Executing system the system external command: ' + shell_command
        self.__process = Popen(shell_command, shell=True, stdout=PIPE, stderr=PIPE)
        if wait_cmd == True:
            self.__process.wait()
        stdout, stderr = self.__process.communicate()
        return stdout, stderr

    def print_output(self, communicates_message):
        for message in communicates_message:
            print message
