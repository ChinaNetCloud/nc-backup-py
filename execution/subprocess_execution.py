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
        # self.stream_watcher('stdout-watcher', self.__process.stdout)
        # print self.__process.stdout
        # print self.__process.stderr
        # self.__process.wait()
        # std_out = Thread(target=self.stream_watcher, name='stdout-watcher',
        #        args=('STDOUT', self.__process.stdout)).start()
        # std_err = Thread(target=self.stream_watcher, name='stderr-watcher',
        #        args=('STDERR', self.__process.stderr)).start()
        #
        # printer_proc = Thread(target=self.__printer, name='printer').start()
        # if std_out is not None:
        #     std_out.join()
        #     std_err.join()
        #     printer_proc.join()
    def print_output(self,communicates_message):
        for message in communicates_message:
            print message


    def stream_watcher(self, identifier, stream):

        for line in stream:
            self.__io_q.put((identifier, line))

        # if not stream.closed:
        #     stream.close()

    def __printer(self):
        while True:
            try:
                # Block for 1 second.
                item = self.__io_q.get(True, 1)
            except Empty:
                # No output in either streams for a second. Are we done?
                if self.__process.poll() is not None:
                    break
            else:
                if item is not None and item is not '':
                    identifier, line = item
                    print identifier + ':', line
                # else:
                #     print the exe

    @staticmethod
    def without_none(self, list_output=None):
        if list_output is not None or list_output is not '':
            without_none = (line for line in list_output if line not in [None, ''])
            for line in without_none:
                print line
        else:
            print 'the output (STDOUT and STDERR) is empty after executing script'
# obj_test = SubprocessExecution.main_execution_function(SubprocessExecution(),'lasds -lah')