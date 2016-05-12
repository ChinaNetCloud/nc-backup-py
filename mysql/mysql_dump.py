#!env python
import argparse
import time
import sys
from subprocess import Popen
from subprocess import PIPE


class mydump:
    def __init__(self):
        self.SCRIPT_PREFIX="mydump"
        self.MYSQLDUMP="/usr/bin/mysqldump"
        self.MYSQL="/usr/bin/mysql"
        self.args_list=self.__get_parameters()
        self.BACKUP_FOLDER=self.args_list.LOCAL_BACKUP+'/'+self.SCRIPT_PREFIX
        self.PREFIX_BACKUP=time.strftime('%Y%m%d',time.localtime(time.time()))+"_"+self.args_list.HOSTNAME

    def __get_parameters(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('--HOSTNAME', type=str, help='Hostname', required=True,action="store")
        parser_object.add_argument('--LOCAL_BACKUP', type=str, help='Local backup folder', required=True,action="store")
        parser_object.add_argument('--CONF_PATH', type=str, help='Configuration file path', required=True,action="store")
        parser_object.add_argument('--CREDENTIAL_PATH', type=str, help='Credential file path', required=True,action="store")
        parser_object.add_argument('--DATA_DIR', type=str, help='Data dir path', required=True,action="store")
        parser_object.add_argument('--MY_INSTANCES', type=str, help='Instance port', required=True,action="store")
        parser_object.add_argument('--LOG', type=str, help='Log path', required=True,action="store")
        args_list = parser_object.parse_args()
        return args_list

    def get_instanceinfo(self,MY_INSTANCE_NAME):
        if MY_INSTANCE_NAME=="3306":
            credential_file=self.args_list.CREDENTIAL_PATH[0]
            MYSQL_DATA_DIR=self.args_list.DATA_DIR[0]
            print "---- MySQL Instance Data Dir: "+MYSQL_DATA_DIR+" ----"
            MYSQLDUMP_AND_CREDS="sudo mysqldump --defaults-extra-file="+credential_file
            MYSQL_AND_CREDS="sudo mysql --defaults-extra-file="+credential_file
        else:
            credential_file=self.args_list.CREDENTIAL_PATH[1]
            MYSQL_DATA_DIR=self.args_list.DATA_DIR[1]
            print "---- MySQL Instance Data Dir: "+MYSQL_DATA_DIR+" ----"
            MYSQLDUMP_AND_CREDS="sudo mysqldump --defaults-extra-file="+credential_file
            MYSQL_AND_CREDS="sudo mysql --defaults-extra-file="+credential_file
        return MYSQL_DATA_DIR,MYSQLDUMP_AND_CREDS,MYSQL_AND_CREDS

    def log_rotate(self,MYSQL_AND_CREDS):
        _SQL1="\! print '------------ Flushing logs ----------'flush logs;\! print\! print '---- Show master status ----' SHOW MASTER STATUS;\! print\! print '---- Show slave status ----'SHOW SLAVE STATUS \G\! print"
        command2=MYSQL_AND_CREDS+" -e "+_SQL1+" >/dev/null"
        rotate_stdout,rotate_stderr=Popen(command2, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        return rotate_stdout,rotate_stderr

    def run_backup(self,MYSQL_AND_CREDS,MYSQLDUMP_AND_CREDS,BACKUP_FOLDER,PREFIX,SCRIPT_PREFIX,MY_INSTANCE_NAME):
        command1=MYSQL_AND_CREDS+" -e 'show databases' | sed '/Database/d' | grep -v 'information_schema' | grep -v 'performance_schema'"
        stdout, stderr = Popen(command1, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        for DB_NAME in stdout.split('\n')[:-1]:
            _SQL2="\"USE information_schema; SELECT TABLE_NAME FROM TABLES WHERE TABLE_SCHEMA='"+DB_NAME+"' AND TABLE_TYPE= 'BASE TABLE' AND ENGINE NOT like 'innodb';\""
            command3=MYSQLDUMP_AND_CREDS+" --opt --routines --triggers --events --flush-privileges --skip-add-drop-table --master-data=2 --dump-date --databases "+DB_NAME+"|sudo gzip > "+BACKUP_FOLDER+"/"+PREFIX+"_"+SCRIPT_PREFIX+"_"+MY_INSTANCE_NAME+"_"+DB_NAME+".sql.gz"
            command4=MYSQLDUMP_AND_CREDS+" --opt --routines --triggers --events --flush-privileges --skip-add-drop-table --master-data=2 --single-transaction  --skip-add-locks --skip-lock-tables --dump-date --databases "+DB_NAME+" | sudo gzip > "+BACKUP_FOLDER+"/"+PREFIX+"_"+SCRIPT_PREFIX+"_"+MY_INSTANCE_NAME+"_"+DB_NAME+".sql.gz"
            print "---- Backing up Instance: "+MY_INSTANCE_NAME+" Database : "+DB_NAME+" ---- "
            command5=MYSQL_AND_CREDS+" -e "+_SQL2+"|grep -v TABLE|wc -l"
            stdout2, stderr = Popen(command5, shell=True, stdout=PIPE, stderr=PIPE).communicate()
            if stdout2!=0:
                print "---- "+DB_NAME+" has MYISAM TABLES , using DUMP backup method ---- "
                backup_stdout,backup_stderr=Popen(command3, shell=True,stdout=PIPE, stderr=PIPE).communicate()
            else:
                print "---- "+DB_NAME+" has all InnoDB tables , using InnoDB backup method ---- "
                backup_stdout,backup_stderr=Popen(command4, shell=True,stdout=PIPE, stderr=PIPE).communicate()
        print "---- Backup Done ---- "
        return backup_stdout,backup_stderr

    def backup_logs(self,MYSQL_DATA_DIR,BACKUP_FOLDER,PREFIX,SCRIPT_PREFIX,MY_INSTANCE_NAME):
        j=""
        command6="ls -l "+MYSQL_DATA_DIR+"| grep 'mysql-bin' | awk '{ print $NF }'"
        stdout6, stderr6 = Popen(command6, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        for i in stdout6.split('\n')[:-1]:
            j=j+" "+MYSQL_DATA_DIR+i
        command7="sudo tar czCf / "+BACKUP_FOLDER+"/"+PREFIX+"_"+SCRIPT_PREFIX+"_"+MY_INSTANCE_NAME+".bin-log.gz j"
        logbak_stdout,logbak_stderr=Popen(command7, shell=True, stdout=PIPE, stderr=PIPE).communicate()
        return logbak_stdout,logbak_stderr


def main():

    saveout = sys.stdout
    test=mydump()
    sys.out=test.args_list.LOG

    for MY_INSTANCE_NAME in test.args_list.MY_INSTANCES.split(','):
        print "---- Processing instance: "+MY_INSTANCE_NAME+" ----"

        MYSQL_DATA_DIR,MYSQLDUMP_AND_CREDS,MYSQL_AND_CREDS=test.get_instanceinfo(MY_INSTANCE_NAME)

        rotate_stdout,rotate_stderr=test.log_rotate(MYSQL_AND_CREDS)

        backup_stdout,backup_stderr=test.run_backup(MYSQL_AND_CREDS,MYSQLDUMP_AND_CREDS,test.BACKUP_FOLDER,test.PREFIX_BACKUP,test.SCRIPT_PREFIX,MY_INSTANCE_NAME)

        logbak_stdout,logbak_stderr=backup_logs(MYSQL_DATA_DIR,test.BACKUP_FOLDER,test.PREFIX,test.SCRIPT_PREFIX,MY_INSTANCE_NAME)

    sys.stdout=saveout



if __name__ == "__main__":
    main()