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

    @staticmethod
    def test_aws_connectivity(home_path, bucket_name):
        aws_s3_ls_command = 'aws s3 ls'
        sys.path.append(home_path)
        from execution.subprocess_execution import SubprocessExecution
        result_aws_s3_ls = SubprocessExecution.main_execution_function(SubprocessExecution(), aws_s3_ls_command)
        # print result_aws_s3_ls
        # print type(result_aws_s3_ls[1])
        # print bucket_name
        # print result_aws_s3_ls[1].find(bucket_name)
        # print type(result_aws_s3_ls[1].find(bucket_name))
        # print result_aws_s3_ls[0]
        if result_aws_s3_ls[0] == 255:
            return 'No credentials'
        elif result_aws_s3_ls[0] == 0 and result_aws_s3_ls[1].find(bucket_name) is -1:
            return 'Bucket not Found'
        return 'Ok'

    def upload_content(self, mypath_to_dir, bucket, client_host_name, upload_command='aws s3 cp',
                       remove_objective='False', aws_s3_test=True):
        if upload_command is None:
            upload_command = 'aws s3 cp'
        aws_and_bucket_test = self.test_aws_connectivity(self.__home_path, bucket)
        print aws_and_bucket_test
        if aws_s3_test == True and aws_and_bucket_test == 'No credentials':
            print 'The can not execute AWS CLI test; please check installation and credentials. ' \
                  'Stopping execution of AWS upload'
            exit(1)
        elif aws_s3_test == True and aws_and_bucket_test == 'Bucket not Found':
            print 'Can not find the AWS bucket name:'+ bucket +' Please check configs and try again'
            exit(1)
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
                # try:
                tmp_execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), aws_command)
                # except
                # print tmp_execution_message
                time_retry = time_retry * count
                if tmp_execution_message[0] == 0:
                    print 'Upload attempt ' + str(count) + ' successful.'
                    break
                elif tmp_execution_message[0] == 127:
                    print "Error with AWS CLI binary. Is it installed?"
                    break
                # NEED TO DETERMINE: is
                # elif tmp_execution_message[0] == 1:
                #     print "Error with AWS CLI binary. Is it installed?"
                #     break
                else:
                    print 'Upload attempt number: ' + str(count) + ' FAILED for: ' + aws_command
                    print 'StdOut: ' + str(tmp_execution_message[0])
                    print 'StdErr: ' + str(tmp_execution_message[0])
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
        print 'Trying uploading to Aliyun OSS bucket:'
        if bucket is not None and bucket != '':
            print bucket
        files_to_upload = [f for f in listdir(mypath_to_dir) if isfile(join(mypath_to_dir, f))]
        import oss2
        credential_dict = self.__read_credentials_from_file(credentials_file)
        if bucket is not None and bucket != '':
            credential_dict['bucket'] = bucket
        auth = oss2.Auth(credential_dict['access_id'], credential_dict['access_key'])

        bucket = oss2.Bucket(auth, credential_dict['host'], credential_dict['bucket'])
        execution_message = []
        for file_to_upload in files_to_upload:
            tmp_result_execution = ''
            local_file = mypath_to_dir + '/' + file_to_upload
            # print local_file
            count = 1
            time_retry = 60
            while count <= 5:
                # try:
                tmp_result_execution = bucket.put_object_from_file (client_host_name + '/' + file_to_upload, local_file)
                # except:
                #     print 'Attempt failed'
                # print('status={0}, request_id={1}'.format(e.status, e.request_id))
                time_retry = time_retry * count
                if tmp_result_execution and tmp_result_execution.status == 200:
                    message_return = 'Status: ' + str(tmp_result_execution.status) + ' Request ID: ' + \
                                     str(tmp_result_execution.request_id) + tmp_result_execution.etag
                    status_success = 0
                    print 'Upload attempt ' + str(count) + ' successful.'
                    break
                else:
                    status_success = 1
                    print 'Upload attempt number: ' + str(count) + ' FAILED for: ' + local_file
                    print tmp_result_execution
                    # print tmp_result_execution.headers
                    print 'We will wait for: ' + str(time_retry / 60) + ' minute(s) before upload attempt number: ' + \
                          str(count + 1)
                    time.sleep(time_retry)
                count = count + 1
            execution_message.append((status_success, message_return, ''))

        sys.path.append(self.__home_path)
        from execution.subprocess_execution import SubprocessExecution
        if remove_objective == 'True' or  remove_objective == True:
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
                    myvars[name.strip()] = str(var).strip().rstrip()

        return myvars


class SSHStorage(Storage):
    def __init__(self, home_path=''):
        self.__home_path = home_path

    def upload_content(self, key_):
        pass
        """import scp

            client = scp.Client(host=host, user=user, keyfile=keyfile)
            # or
            client = scp.Client(host=host, user=user)
            client.use_system_keys()
            # or
            client = scp.Client(host=host, user=user, password=password)

            # and then
            client.transfer('/etc/local/filename', '/etc/remote/filename')
        """
