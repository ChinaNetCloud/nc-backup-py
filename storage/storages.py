import sys


from os import listdir
from os.path import isfile, join


class Storage:

    def list_content(self):
        print "Listing directory content"

    def upload_content(self):
        print 'Uploading to storage'

    def remove_content(self):
        print 'General: removing files from storage'

    def check_size_content(self):
        print 'checking the files size'


class AWSS3(Storage):
    def __init__(self, home_path):
        self.__home_path = home_path
        # self.__subprocess_upload = SubprocessExecution()

    def list_content(self):
        print "Listing directory content"

    def upload_content(self, mypath_to_dir, bucket, client_host_name, upload_command='aws s3 cp', remove_objective='False'):
        print 'Uploading to storage S3'
        files_to_upload = [f for f in listdir(mypath_to_dir) if isfile(join(mypath_to_dir, f))]
        sys.path.append(self.__home_path)
        from execution.subprocess_execution import SubprocessExecution
        execution_message = []
        for file_to_upload in files_to_upload:
            aws_command = upload_command + ' '+ mypath_to_dir + '/' + file_to_upload + ' s3://'+ bucket + '/' + client_host_name + '/' + file_to_upload
            # print aws_command
            execution_message.append(SubprocessExecution.main_execution_function(SubprocessExecution(), aws_command))
            # SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        if remove_objective:
            execution_message.append(SubprocessExecution.main_execution_function(SubprocessExecution(), 'rm -rf ' + mypath_to_dir))
            # SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        # print execution_message
        return execution_message

    def remove_content(self):
        print 'S3: removing files from storage'

    def check_size_content(self):
        print 'checking the files size'
