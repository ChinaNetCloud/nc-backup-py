import argparse
import sys



class StorageExecution:

    def storage_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', '--TARGETS', type=str
                                   , help='Objectives to encrypt', required=False)
        parser_object.add_argument('-l', '--LOCAL_BACKUP', type=str
                                   , help='Objectives to encrypt', required=True)
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str
                                   , help='Path to the whole project folder, '
                                          'to include other libruaries', required=True)
        parser_object.add_argument('-D', '--DESTINATION', type=str
                                   , help='Backup destination: local, s3, oss, etc', required=True)
        parser_object.add_argument('-b', '--BUCKET_NAME', type=str
                                   , help='Backup destination e.g: nc-backup-kr', required=False)
        parser_object.add_argument('-hn', '--HOSTNAME', type=str
                                   , help='Server name (client Host Name) e.g: nc-backup-kr', required=True)
        parser_object.add_argument('-u', '--UPLOAD_COMMAND', type=str
                                   , help='AWS upload command', required=False)
        parser_object.add_argument('-R', '--REMOVE_OBJECTIVES', '--REMOVE_TARGETS', type=str
                                   , help='Remove Encrypted files and folder after execution', required=False)
        parser_object.add_argument('-A', '--ALIYUN_CREDENTIALS', type=str
                                   , help='Remove Encrypted files and folder', required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def iterate_resut(self, uploads_to_cloud):
        succesful = 0
        count_file = 1
        print uploads_to_cloud
        for upload_to_cloud in uploads_to_cloud:
            if upload_to_cloud[0] is not 0:
                print 'upload of file number ' + str(
                    count_file) + ' failed to upload.'
                exit(1)
            count_file = count_file + 1

if __name__ == "__main__":
    storage_cmd = StorageExecution.storage_commands(StorageExecution())
    sys.path.append(storage_cmd.HOME_FOLDER)
    from tools.filesystem_handling import FilesystemHandling
    from execution.subprocess_execution import SubprocessExecution
    from execution.config_parser import ConfigParser
    if str(storage_cmd.DESTINATION) not in ['s3', 'oss', 'ssh', 'local', 'azure']:
        print 'Not supported storage destination: ' + str(storage_cmd.DESTINATION)
        exit(1)

    if not ConfigParser.check_exists(ConfigParser(), storage_cmd.REMOVE_OBJECTIVES):
        storage_cmd.REMOVE_OBJECTIVES = 'True'
    if not ConfigParser.check_exists(ConfigParser(), storage_cmd.OBJECTIVES):
        storage_cmd.OBJECTIVES = '/opt/backup/encrypted'
    print 'Executing backup files type: ' + storage_cmd.DESTINATION
    if storage_cmd.DESTINATION == 'local':
        command_move = 'mv ' + storage_cmd.OBJECTIVES + '/* ' + storage_cmd.LOCAL_BACKUP
        FilesystemHandling.create_directory(storage_cmd.LOCAL_BACKUP)
        ExecuteBackup = SubprocessExecution.main_execution_function(SubprocessExecution(), command_move)
        if storage_cmd.REMOVE_OBJECTIVES == 'True':
            FilesystemHandling.remove_files(storage_cmd.OBJECTIVES)
    elif storage_cmd.DESTINATION == 's3':
        print "calling S3 storage upload functions"
        from storages import AWSS3
        uploads_to_s3 = AWSS3.upload_content(AWSS3(storage_cmd.HOME_FOLDER),storage_cmd.OBJECTIVES,
                                            storage_cmd.BUCKET_NAME, storage_cmd.HOSTNAME,
                                            storage_cmd.UPLOAD_COMMAND, storage_cmd.REMOVE_OBJECTIVES)
        succesful = 0
        count_file = 1
        if uploads_to_s3:
            StorageExecution.iterate_resut(StorageExecution(), uploads_to_s3)
        else:
            print 'Executing OSS upload retuned a None result'

    elif storage_cmd.DESTINATION == 'oss':
        print "calling OSS storage upload functions"
        from storages import AliyunOSS
        print storage_cmd.BUCKET_NAME
        uploads_to_oss = AliyunOSS.upload_content(AliyunOSS(storage_cmd.HOME_FOLDER), storage_cmd.ALIYUN_CREDENTIALS,
                                                  storage_cmd.OBJECTIVES, storage_cmd.BUCKET_NAME,
                                                  storage_cmd.HOSTNAME, storage_cmd.REMOVE_OBJECTIVES)
        if uploads_to_oss:
            StorageExecution.iterate_resut(StorageExecution(), uploads_to_oss)
        else:
            print 'Executing OSS upload retuned a None result'

    elif storage_cmd.DESTINATION == 'ssh':
        print "calling SSH storage upload functions"
