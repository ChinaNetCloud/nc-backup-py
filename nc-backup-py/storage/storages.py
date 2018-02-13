import sys
import time


from os import listdir
from os.path import isfile, join
from tools.filesystem_handling import remove_objectives, FilesystemHandling

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

    def execute(self):
        """Execute commands after subtitution."""
        from execution.subprocess_execution import SubprocessExecution
        files_to_upload = [f for f in listdir(self.__args.OBJECTIVES)
                           if isfile(join(self.__args.OBJECTIVES, f))]

        # Not very elegant, change later.
        if self.__args.DESTINATION == 'local':
            FilesystemHandling.create_directory(
                self.__custom_command_dict['LOCAL_BACKUP']
                )

        with open() as f:
            f.writelines(files_to_upload)
        # Loop through files in "objectives".
        for file_to_upload in files_to_upload:
            self.__custom_command_dict["file"] = file_to_upload
            count = 1
            time_retry = 60
            execution_message = []

            while count <= 5:
                print 'Trying upload attempt number: ' + str(count)
                try:
                    command = self.__args.UPLOAD_COMMAND_TEMPLATE % self.__custom_command_dict
                except Exception, e:
                    print "Check your ARGS_DICT parameter."
                    print "The upload string was :"
                    print self.__args.UPLOAD_COMMAND_TEMPLATE
                    print "If you are using default templates check the templates file at:"
                    print "%s/%s" % (self.__args.HOME_FOLDER,
                                     self.__args.DEFAULT_TEMPLATE_FILE)
                    print e
                    exit(1)
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

        if self.__args.REMOVE_OBJECTIVES:
            remove_objectives(objectives=self.__args.OBJECTIVES,
                              remove_objectives=self.__args.REMOVE_OBJECTIVES)
        return execution_message
