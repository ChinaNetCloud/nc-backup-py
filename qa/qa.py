import os
import pwd


class QA:
    def __init__(self, logger=None):
        print 'Checking QA according to configs'
        self.__logger = logger

    def config_plugin(self):
        print 'Size calculation plugin\'s config is NOT in use'

    def works_execution(self):
        self.check_user()

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
            result_log = 'The servers does not follow our user policy standards, please FIX user: ' + self.__username
            self.__logger.warning(result_log)

    def check_user(self):
        print 'Checking user.'
        self.__username = pwd.getpwuid(os.getuid()).pw_gecos
        self.__gid = os.getgid()
        self.__uid = os.geteuid()
        if self.__username == 'ncbackup' and int(self.__gid) > 0 and int(self.__uid) > 0:
            self._result_user_eval = True
        else:
            self._result_user_eval = False

    def check_os_paths(self):
        print 'IMPLEMENT'
