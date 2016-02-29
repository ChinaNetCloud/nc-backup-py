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
        Thread(target=self.stream_watcher, name='stdout-watcher',
               args=('STDOUT', self.__process.stdout)).start()
        Thread(target=self.stream_watcher, name='stderr-watcher',
               args=('STDERR', self.__process.stderr)).start()
        Thread(target=self.printer, name='printer').start()

    def stream_watcher(self, identifier, stream):

        for line in stream:
            self.__io_q.put((identifier, line))

        if not stream.closed:
            stream.close()

    def printer(self):
        while True:
            try:
                # Block for 1 second.
                item = self.__io_q.get(True, 1)
            except Empty:
                # No output in either streams for a second. Are we done?
                if self.__process.poll() is not None:
                    break
            else:
                identifier, line = item
                print identifier + ':', line

# obj_test = SubprocessExecution.main_execution_function(SubprocessExecution(),'lasds -lah')