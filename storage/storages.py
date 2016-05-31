import sys
import time


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
    def __init__(self, home_path=''):
        self.__home_path = home_path
        # self.__subprocess_upload = SubprocessExecution()

    def list_content(self):
        print "Listing directory content"

    def upload_content(self, mypath_to_dir, bucket, client_host_name, upload_command='aws s3 cp',
                       remove_objective='False'):
        print 'Uploading to storage S3'
        files_to_upload = [f for f in listdir(mypath_to_dir) if isfile(join(mypath_to_dir, f))]
        sys.path.append(self.__home_path)
        from execution.subprocess_execution import SubprocessExecution
        execution_message = []
        for file_to_upload in files_to_upload:
            aws_command = upload_command + ' '+ mypath_to_dir + '/' + file_to_upload + ' s3://'+ bucket + '/' \
                          + client_host_name + '/' + file_to_upload
            count = 1
            time_retry = 60
            while count <= 5:
                print 'Trying upload attempt number: ' + str(count)
                tmp_execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), aws_command)
                # print tmp_execution_message
                time_retry = time_retry * count
                if tmp_execution_message[0] == 0:
                    print 'Upload attempt ' + str(count) +' successful.'
                    break
                else:
                    print 'Upload attempt number: ' + str(count) + ' FAILED for: ' + aws_command
                    print 'StdOut: ' + str(tmp_execution_message[0])
                    print 'StdErr:' + str(tmp_execution_message[0])
                    print 'We will wait for: ' + str(time_retry/60) + ' minute(s) before upload attempt number: ' + \
                          str(count + 1)
                    time.sleep(time_retry)
                count = count + 1
            execution_message.append(tmp_execution_message)
        if remove_objective == 'True':
            execution_message.append(SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                 'rm -rf ' + mypath_to_dir))
        return execution_message

    def remove_content(self):
        print 'S3: removing files from storage'

    def check_size_content(self):
        print 'checking the files size'

class AliyunOSS(Storage):
    def __init__(self, home_path=''):
        self.__home_path = home_path

        # self.__subprocess_upload = SubprocessExecution()

    def list_content(self):
        print "Listing directory content"

    def upload_content(self, credentials_file, mypath_to_dir, bucket='', client_host_name='', remove_objective='False'):
        print 'Trying uploading to Aliyun OSS bucket: ' + bucket
        files_to_upload = [f for f in listdir(mypath_to_dir) if isfile(join(mypath_to_dir, f))]
        import oss2
        credential_dict = self.__read_credentials_from_file(credentials_file)
        print credential_dict['access_key'], credential_dict['access_id'], credential_dict['bucket'], credential_dict['host']
        # if client_host_name != '' and client_host_name is str:
        #     credential_dict['host'] =
        if bucket != '' and bucket is str:
            credential_dict['bucket'] = bucket

        auth = oss2.Auth(credential_dict['access_id'], credential_dict['access_key'])
        # print auth
        service = oss2.Service(auth, credential_dict['host'])
        # print service
        print([b.name for b in oss2.BucketIterator(service)])
        #
        # bucket = oss2.Bucket(auth, 'http://oss-cn-hangzhou.aliyuncs.com', 'bucket')
        # # bucket.create_bucket(oss2.models.BUCKET_ACL_PRIVATE)
        #
        # bucket.put_object_from_file('remote.txt', 'local.txt')
        # print bucket
        #
        # print([b.name for b in oss2.BucketIterator(service)])
        execution_message = []
        sys.path.append(self.__home_path)
        from execution.subprocess_execution import SubprocessExecution
        if remove_objective == 'True':
            execution_message.append(SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                 'rm -rf ' + mypath_to_dir))

        return execution_message

    def remove_content(self):
        print 'S3: removing files from storage'


    def check_size_content(self):
        print 'checking the files size'

    def __read_credentials_from_file(self, file_to_read):
        print 'Now we read the Aliyun credentials from the file: ' + file_to_read
        myvars = {}
        with open(file_to_read, 'r') as file_loaded:
            print file_loaded.name
            for line in file_loaded:
                if line  and line is not '' and '[' not in line and ']' not in line and not line.startswith('#'):
                    name, var = line.partition("=")[::2]
                    myvars[name.strip()] = str(var)

        return myvars

    # def find_between(s, first, last):
    #     try:
    #         start = s.index(first) + len(first)
    #         end = s.index(last, start)
    #         return s[start:end]
    #     except ValueError:
    #         return ""