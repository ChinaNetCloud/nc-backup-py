import sys
import time


from os import listdir
from os.path import isfile, join
from tools.filesystem_handling import remove_objectives

class Storage:
    """"""

    def __init__(self, storage_cmd):
        """Get and store arguments."""
        self.__args = storage_cmd
        self.__checkArgs()

    def __checkArgs(self):
        self.__custom_command_dict = eval(self.__args.ARGS_DICT)
        self.__custom_command_dict["OBJECTIVES"] = self.__args.OBJECTIVES
        self.__custom_command_dict["HOSTNAME"] = self.__args.HOSTNAME

    def list_content(self):
        print "Listing directory content"

    def upload_content(self):
        print 'Uploading to storage'

    def remove_content(self):
        print 'General: removing files from storage'

    def check_size_content(self):
        print 'checking the files size'

    def execute(self):
        from execution.subprocess_execution import SubprocessExecution
        files_to_upload = [f for f in listdir(self.__args.OBJECTIVES)
                           if isfile(join(self.__args.OBJECTIVES, f))]
        for file_to_upload in files_to_upload:
            self.__custom_command_dict["file"] = file_to_upload
            count = 1
            time_retry = 60
            execution_message = []

            while count <= 5:
                print 'Trying upload attempt number: ' + str(count)
                command = self.__args.UPLOAD_COMMAND_TEMPLATE % self.__custom_command_dict
                print "Executing external command: %s " % command
                tmp_execution_message = SubprocessExecution.main_execution_function(
                    SubprocessExecution(),
                    command)
                count = count + 1
                time_retry = time_retry * count
                if tmp_execution_message[0] == 0:
                    print 'Upload attempt ' + str(count) + ' successful.'
                    break
                else:
                    print 'Upload attempt number: ' + str(count) + ' FAILED for: ' + command
                    print 'StdOut: ' + str(tmp_execution_message[0])
                    print 'StdErr: ' + str(tmp_execution_message[0])
                    print 'We will wait for: ' + str(time_retry/60) + ' minute(s) before upload attempt number: ' + \
                          str(count + 1)
                    time.sleep(time_retry)
            execution_message.append(tmp_execution_message)

        return execution_message
