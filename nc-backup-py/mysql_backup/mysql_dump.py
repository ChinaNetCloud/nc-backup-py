import argparse
import time
import sys
import os
import re


from subprocess import Popen
from subprocess import PIPE

'''
This code file was developed originally  by Randy Yang.
Abel Guzman is supposed to make it work
and make improvements in:
- Coding standards
- Decopling code
- Command independence from script (Exclude)
- bing log not active should not make backup fiale, just warn.
'''

class mydump:
    def __init__(self):
        self.args_list = self.__get_parameters()
        if self.args_list.PREFIX_FOLDER:
            self.script_prefix = self.args_list.PREFIX_FOLDER
        else:
            self.script_prefix = "mydump"
        if self.args_list.MYSQL_DUMP_BINARY:
            self.mysql_dump_binary = self.args_list.MYSQL_DUMP_BINARY
        else:
            self.mysql_dump_binary = "/usr/bin/mysqldump"
        if self.args_list.MYSQL_BINARY:
            self.MYSQL = self.args_list.MYSQL_BINARY
        else:
            self.MYSQL = "/usr/bin/mysql"
        if self.args_list.TAR_COMMAND:
            self.tar_command = self.args_list.TAR_COMMAND
        else:
            self.tar_command = 'sudo /bin/tar czf'
        sys.path.append(self.args_list.HOME_FOLDER)
        from execution.config_parser import ConfigParser
        if not ConfigParser.check_exists(ConfigParser(), self.args_list.MY_INSTANCES):
            self.args_list.MY_INSTANCES = '3306'
        if not ConfigParser.check_exists(ConfigParser(), self.args_list.DESTINATION):
            self.args_list.DESTINATION = '/opt/backup'
        self.DESTINATION = self.args_list.DESTINATION + '/'+self.script_prefix
        self.PREFIX_BACKUP = time.strftime('%Y%m%d',time.localtime(time.time())) + "_"+self.args_list.HOSTNAME
        if self.DESTINATION:
            sys.path.append(self.args_list.HOME_FOLDER)
            # from compression.zip_compression import ZipCompression
            from execution.subprocess_execution import SubprocessExecution
            if not os.path.isdir(self.DESTINATION):
                create_dir_cmd = 'mkdir ' + self.DESTINATION
                execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), create_dir_cmd, True)
                if execution_mkdir[0] != 0:
                    print 'Could Not create directory with command: ' + create_dir_cmd
                    print 'Error code: ' + str(execution_mkdir[0])

    def __get_parameters(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('--HOSTNAME', type=str, help='Hostname', required=True,action="store")
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str
                                   , help='Script home folder required(from where the master script runs)',
                                   required=True)
        parser_object.add_argument('--DESTINATION', type=str, help='Local backup folder', required=False, action="store")
        parser_object.add_argument('--CREDENTIAL_PATH', type=str, help='Credential file path',
                                   required=False,action="store")
        parser_object.add_argument('--DATA_DIR', type=str, help='Data dir path', required=False,action="store")
        parser_object.add_argument('--MY_INSTANCES', type=str, help='Instance port', required=False, action="store")
        parser_object.add_argument('--BINLOG_PATH', type=str, help='Bin Log folder', required=False, action="store")
        parser_object.add_argument('--BINLOG_DAYS', type=str, help='Bin Log folder', required=False)
        parser_object.add_argument('--BINLOG_FILE_PREFIX', type=str, help='Bin Log file prefix',
                                   required=False, action='store')
        parser_object.add_argument('--MYSQL_DUMP_BINARY',type=str, help='MySQL Dump Binarey',  required=False)
        parser_object.add_argument('--MYSQL_BINARY', type=str, help='MySQL Binarey', required=False)
        parser_object.add_argument('--PREFIX_FOLDER', type=str, help='Prefix or folder to use', required=False)
        parser_object.add_argument('--TAR_COMMAND', type=str, help='tar command to use', required=False)
        parser_object.add_argument('--EXCLUDE_DB', type=str, help='exclude database', required=False)
        parser_object.add_argument('--EXCLUDE_TABLE', type=str, help='exclude database table', required=False)
        # Argument to be implemented Name PIPE
        # parser_object.add_argument('--PIPE', type=str, help='use as pipe true|false, default is false', required=False)

        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def get_instanceinfo(self,MY_INSTANCE_NAME):
        if MY_INSTANCE_NAME=="3306":
            credential_file=self.args_list.CREDENTIAL_PATH.split()[0]
            MYSQL_DATA_DIR=self.args_list.DATA_DIR.split()[0]
            print "---- MySQL Instance Data Dir: "+MYSQL_DATA_DIR+" ----"
            mysql_dump_and_credentials = self.mysql_dump_binary + " --defaults-extra-file="+credential_file
            mysql_and_credentials = self.MYSQL + " --defaults-extra-file="+credential_file
        else:
            credential_file=self.args_list.CREDENTIAL_PATH.split()[0]
            MYSQL_DATA_DIR=self.args_list.DATA_DIR.split()[1]
            print "---- MySQL Instance Data Dir: "+MYSQL_DATA_DIR+" ----"
            mysql_dump_and_credentials = self.mysql_dump_binary + " --defaults-extra-file="+credential_file
            mysql_and_credentials = self.MYSQL + " --defaults-extra-file=" + credential_file
        return MYSQL_DATA_DIR,mysql_dump_and_credentials, mysql_and_credentials

    def log_rotate(self,mysql_and_credentials):
        _SQL1="flush logs; SHOW MASTER STATUS; SHOW SLAVE STATUS \G "
        command2=mysql_and_credentials + " -e '"+_SQL1+"' >/dev/null"
        print command2
        rotate_stdout,rotate_stderr=Popen(command2, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        # print rotate_stdout,rotate_stderr
        return rotate_stdout,rotate_stderr

    def run_backup(self,mysql_and_credentials, mysql_dump_and_credentials, DESTINATION, PREFIX, script_prefix,
                   MY_INSTANCE_NAME):
        chain_exclude_tables = ""
        if self.args_list.EXCLUDE_TABLE:
            list_tables = self.args_list.EXCLUDE_TABLE.split()
            for table in list_tables:
                chain_exclude_tables += " --ignore-table=" + table
        else:
            list_tables = ""
            chain_exclude_tables = ""

        command1=mysql_and_credentials + " -e 'show databases' | sed '/Database/d' | grep -v 'information_schema' " \
                                         "| grep -v 'performance_schema' | grep -v 'sys'"
        stdout, stderr = Popen(command1, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        db_all = stdout.split('\n')[:-1]
        chain_exclude_dbs = ""
        if self.args_list.EXCLUDE_DB:
            list_dbs = self.args_list.EXCLUDE_DB.split()
        else:
            list_dbs = []
        i = None
        db_include = [ i for i in db_all if i not in list_dbs ]
        # get Mysql Version.
        mysql_version_command = mysql_and_credentials + " --version"
        stdout_mysql_version, stderr_mysql_version = Popen(mysql_version_command, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        if '5.7' in stdout_mysql_version:
            mysql_version = '5.7'
        elif '5.6' in stdout_mysql_version:
            mysql_version = '5.6'
        elif '5.5' in stdout_mysql_version:
            mysql_version = '5.5'
        else:
            mysql_version = 'legacy'

        if not db_include:
            return "No databases found.", ''

        for DB_NAME in db_include:
            _SQL2="\"USE information_schema; SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA='" + \
                  DB_NAME + "' AND TABLE_TYPE= 'BASE TABLE' AND ENGINE NOT like 'innodb';\""
            initial_command = " --opt --routines --triggers --events --flush-privileges " \
                                         "--skip-add-drop-table"
            if mysql_version == '5.7':
                set_specific_parameters = ' --set-gtid-purged=OFF'
            else:
                set_specific_parameters = ''
            if mysql_version == '5.5' or mysql_version == '5.6' or mysql_version == '5.7':
                set_specific_parameters += ' --single-transaction'
            # MYISAM Commanf without  --master-data=2
            command3=mysql_dump_and_credentials + initial_command + set_specific_parameters + \
                     " --dump-date --databases " + \
                     DB_NAME + chain_exclude_tables + "| gzip > " + DESTINATION + "/" + PREFIX + "_" + script_prefix + \
                     "_" + MY_INSTANCE_NAME + "_" + DB_NAME+".sql.gz"
            # InnoDB command with --master-data=2
            command4=mysql_dump_and_credentials + initial_command + set_specific_parameters + \
                     " --master-data=2 --skip-add-locks --skip-lock-tables --dump-date " \
                     "--databases " + DB_NAME + chain_exclude_tables + " | gzip > " \
                     + DESTINATION + "/" + PREFIX + "_" + script_prefix + "_" + MY_INSTANCE_NAME + "_" + DB_NAME + ".sql.gz"
            print "---- Backing up Instance: "+MY_INSTANCE_NAME+" Database : "+DB_NAME+" ---- "
            command5=mysql_and_credentials + " -e "+_SQL2+"|grep -v TABLE|wc -l"
            # print command5
            stdout2, stderr = Popen(command5, shell=True, stdout=PIPE, stderr=PIPE).communicate()
            if stdout2 != 0:
                print "---- "+DB_NAME+" has MYISAM TABLES , using DUMP backup method ---- "
                backup_stdout,backup_stderr=Popen(command3, shell=True,stdout=PIPE, stderr=PIPE).communicate()
            else:
                print "---- "+DB_NAME+" has all InnoDB tables , using InnoDB backup method ---- "
                backup_stdout,backup_stderr=Popen(command4, shell=True,stdout=PIPE, stderr=PIPE).communicate()
        print "---- Backup Done ---- "
        return backup_stdout,backup_stderr

    def backup_logs(self,MYSQL_DATA_DIR,DESTINATION, script_prefix, MY_INSTANCE_NAME,
                    BINLOG_PATH='/var/lib/mysql/data', BINLOG_FILE_PREFIX='mysql-bin', days=2):
        files_strig_list=""
        bin_log_files_list = [BINLOG_PATH + '/' + name for name in os.listdir(BINLOG_PATH) if BINLOG_FILE_PREFIX + '.' in name]
        now = time.time()
        if days is None:
            days = 2
        bin_log_files_list = [file_log for file_log in bin_log_files_list if os.stat(file_log).st_mtime > now - (float(days) * 86400)]
        for i in bin_log_files_list:
            files_strig_list =  files_strig_list + ' ' + i
        command7=self.tar_command + ' ' + str(DESTINATION) + "/" + str(script_prefix) \
                 + "_" + str(MY_INSTANCE_NAME) +".bin-log.tar.gz" + files_strig_list
        print command7
        logbak_stdout,logbak_stderr=Popen(command7, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        return logbak_stdout,logbak_stderr


def main():
    mydump_object=mydump()
    sys.path.append(mydump_object.args_list.HOME_FOLDER)
    from execution.config_parser import ConfigParser


    if not mydump_object.args_list.MY_INSTANCES or mydump_object.args_list.MY_INSTANCES == '':
        mydump_object.args_list.MY_INSTANCES = '3306'
    # Check if a path to credentials was provided or use the default path
    if not ConfigParser.check_exists(ConfigParser(),mydump_object.args_list.CREDENTIAL_PATH):
        mydump_object.args_list.CREDENTIAL_PATH = '/etc/nc-backup-py/mysql_backup.creds'
    if not ConfigParser.check_exists(ConfigParser(),mydump_object.args_list.DATA_DIR):
        mydump_object.args_list.DATA_DIR = '/var/lib/mysql/data'
    if not ConfigParser.check_exists(ConfigParser(), mydump_object.args_list.BINLOG_PATH):
        mydump_object.args_list.BINLOG_PATH = mydump_object.args_list.DATA_DIR
    if not ConfigParser.check_exists(ConfigParser(), mydump_object.args_list.BINLOG_FILE_PREFIX):
        mydump_object.args_list.BINLOG_FILE_PREFIX = 'mysql-bin'

    if mydump_object.args_list.BINLOG_PATH and mydump_object.args_list.BINLOG_PATH != '':
        if not ConfigParser.is_existing_abs_path(ConfigParser(),mydump_object.args_list.BINLOG_PATH):
            print 'The path to bin Log folder does not exits, execution will not contune'
            exit(1)
    else:
        print 'Bin log folder is empty, this parameter is required, execution will not contune'
        exit(1)

    if not mydump_object.args_list.BINLOG_FILE_PREFIX or mydump_object.args_list.BINLOG_FILE_PREFIX == '':
        print 'Bin file name can not be empty, execution will not contune'
        exit(1)

    for MY_INSTANCE_NAME in mydump_object.args_list.MY_INSTANCES.split(','):

        print "---- Processing instance: " + MY_INSTANCE_NAME + " ----"

        MYSQL_DATA_DIR,mysql_dump_and_credentials,mysql_and_credentials=mydump_object.get_instanceinfo(MY_INSTANCE_NAME)
        rotate_stdout,rotate_stderr=mydump_object.log_rotate(mysql_and_credentials)
        print rotate_stdout
        print rotate_stderr
        if rotate_stderr:
            print 'There was an error executing get MySQL Instance function'
            exit(1)
        backup_stdout,backup_stderr=mydump_object.run_backup(mysql_and_credentials,mysql_dump_and_credentials,
                                                             mydump_object.DESTINATION,mydump_object.PREFIX_BACKUP,
                                                             mydump_object.script_prefix,MY_INSTANCE_NAME)
        print backup_stdout
        print backup_stderr
        if backup_stderr:
            print 'There was an error running the dump of the DBs'
            exit(1)
        logbak_stdout,logbak_stderr=mydump_object.backup_logs(MYSQL_DATA_DIR,mydump_object.DESTINATION,
                                                              mydump_object.script_prefix,
                                                              MY_INSTANCE_NAME,
                                                              mydump_object.args_list.BINLOG_PATH,
                                                              mydump_object.args_list.BINLOG_FILE_PREFIX,
                                                              mydump_object.args_list.BINLOG_DAYS)
        print logbak_stdout
        print logbak_stderr


if __name__ == "__main__":
    main()
