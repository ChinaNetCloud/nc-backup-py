import os
import pwd


class QA:
    def __init__(self, logger=None):
        print 'Checking QA according to configs'
        self.__logger = logger
        self.__username = None

    def config_plugin(self):
        print 'Size calculation plugin\'s config is NOT in use'

    def works_execution(self):
        self.__check_user()
        self.__check_os_paths()

    def output(self):
        """Check User running script"""
        header_output_user = '*** Users and group information ***'
        self.__logger.info(header_output_user)
        print header_output_user
        username_log = 'Username: ' + self.__username
        self.__logger.info(username_log)
        print username_log
        gid_user = 'GID: ' + str(self.__gid)
        self.__logger.info(gid_user)
        print gid_user
        uid_user = 'UID: ' + str(self.__uid)
        self.__logger.info(uid_user)
        if self._result_user_eval == True:
            result_log = 'User setup policy is correct'
            self.__logger.info(result_log)
        else:
            result_log = 'Config did not pass QA!. The servers does not follow our user policy standards, ' \
                         'please FIX user: ' + self.__username
            self.__logger.warning(result_log)

    def __check_user(self):
        print 'Checking user.'
        self.__username = pwd.getpwuid(os.getuid()).pw_name
        self.__gid = os.getgid()
        self.__uid = os.geteuid()

        if self.__username == 'ncbackup' and int(self.__gid) > 0 and int(self.__uid) > 0:
            self._result_user_eval = True
        else:
            self._result_user_eval = False

    def __check_os_paths(self, a_dict_configs=None):
        self.dict_configs = {}
        if not a_dict_configs:
            """Config file access"""
            self.dict_configs['file_conf'] = {}
            self.dict_configs['file_conf']['path'] = '/etc/nc-backup-py/conf.json'
            self.dict_configs['file_conf']['owner'] = 'ncbackup'
            self.dict_configs['file_conf']['group'] = 'ncbackup'
            self.dict_configs['file_conf']['permissions'] = '740'
            """Log file permits"""
            self.dict_configs['folder_logs'] = {}
            self.dict_configs['folder_logs']['path'] = '/var/log/nc-backup-py/'
            self.dict_configs['folder_logs']['owner'] = 'ncbackup'
            self.dict_configs['folder_logs']['group'] = 'ncbackup'
            self.dict_configs['folder_logs']['permissions'] = '664'
            """"Source code location"""
            self.dict_configs['folder_code'] = {}
            self.dict_configs['folder_code']['path'] = '/var/lib/nc-backup-py'
            self.dict_configs['folder_code']['owner'] = 'ncbackup'
            self.dict_configs['folder_code']['group'] = 'ncbackup'
            self.dict_configs['folder_code']['permissions'] = '664'
            """Key_file"""
            self.dict_configs['folder_code'] = {}
            self.dict_configs['folder_code']['path'] = '/etc/nc-backup-py/key_file'
            self.dict_configs['folder_code']['owner'] = 'ncbackup'
            self.dict_configs['folder_code']['group'] = 'ncbackup'
            self.dict_configs['folder_code']['permissions'] = '400'

            """MySQL credentials"""
            mysql_credentials_path = '/etc/nc-backup-py/mysql.credentials'
            # if ()
        else:
            self.dict_configs = a_dict_configs
        # print self.dict_configs
        for dict_file_permits in self.dict_configs:
            # print "AA"
            pass
