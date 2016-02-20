#######################################################
# Class Name S3FileTreatment                           #
# Synopsis: Remove files from S3 bucket                #
# +remove_file_group(self,list):list                   #
# +remove_file(string):string                          #
# +get_bucket_usage(string):string                     #
# date       Change                     Who            #
# 2016-01-13 Created delete list & file Abel Guzman    #
#######################################################

import commands


class S3FileTreatment:
    # remove a list of files from s3
    # arg: list of files uri
    # ret: list of results from deletion attempts
    def remove_file_group(self, file_uri_list):
        remove_result = []
        for file_uri in file_uri_list:
            remove_result.append(self.remove_file(file_uri))
        return remove_result

    # remove one file from S3
    # arg: a file uri
    # ret: was deleted successfuly or file not found
    @staticmethod
    def remove_file(file_uri):
        if (commands.getstatusoutput('s3cmd ls ' + file_uri)[1] == ''):
            return 'File: ' + file_uri + ' file not found'
        else:
            commands.getstatusoutput('s3cmd del ' + file_uri)
            return 'File: ' + file_uri + ' successfully removed'

    # get s3 space usage
    # arg: s3 uri
    # ret: size output
    @staticmethod
    def get_bucket_size(s3_uri=''):
        '''
        It will return [[servername,date,s3_file_path]]
        '''
        backup_usage_list = []
        get_cmd = 's3cmd du -H ' + s3_uri
        backup_output = commands.getstatusoutput(get_cmd)
        return backup_output

# Test code
# obj = S3FileTreatment()
# print (obj.get_bucket_size('s3://randy-test-env/'))
# Test delete One File
# print(obj.remove_file('s3://randy-test-env/srv-randy-test-db1/160113_110001_srv-randy-test-db1.test1.txt'))
# Test delete a list of files
# file_list = [
#    's3://randy-test-env/srv-randy-test-db1/160113_110001_srv-randy-test-db1.test1.txt',
#    's3://randy-test-env/srv-randy-test-db1/160113_110001_srv-randy-test-db1.test2.txt',
#    's3://randy-test-env/srv-randy-test-db1/160113_110001_srv-randy-test-db1.test3.txt',
#    's3://randy-test-env/srv-randy-test-db1/160113_110001_srv-randy-test-db1.test4.txt'
#    ]
# print(obj.remove_file_group (file_list))
