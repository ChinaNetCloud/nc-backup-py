from subprocess import Popen
from subprocess import PIPE
from threading import Thread
from Queue import Queue, Empty


class SubprocessExecution:
    __io_q = Queue()
    __process = None

    def main_execution_function(self, shell_command):
        print 'Executing system the system external command: ' + shell_command
        self.__process = Popen(shell_command, shell=True, stdout=PIPE, stderr=PIPE)

        return self.__process.communicate()

    def print_output(self,communicates_message):
        for message in communicates_message:
            print message


