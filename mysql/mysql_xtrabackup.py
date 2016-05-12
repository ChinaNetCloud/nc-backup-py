#!env python
import argparse
import time
import sys
import commands
from subprocess import Popen
from subprocess import PIPE

class xtrabackup:
    def __init__(self):
        self.SCRIPT_PREFIX="xtrabackup"
        self.args_list=self.__get_parameters()
        self.BACKUP_FOLDER=self.args_list.LOCAL_BACKUP+'/'+self.SCRIPT_PREFIX
        self.date=time.strftime('%Y%m%d',time.localtime(time.time()))
        self.PREFIX_BACKUP=time.strftime('%Y%m%d',time.localtime(time.time()))+"_"+self.args_list.HOSTNAME
        self.backup_dir_full=self.args_list.LOCAL_BACKUP+'/'+self.SCRIPT_PREFIX+"_full"
        self.backup_dir_inc=self.args_list.LOCAL_BACKUP+'/'+self.SCRIPT_PREFIX+"_inc"

    def __get_parameters(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('--HOSTNAME', type=str, help='Hostname', required=True,action="store")
        parser_object.add_argument('--LOCAL_BACKUP', type=str, help='Local backup folder', required=True,action="store")
        parser_object.add_argument('--CONF_PATH', type=str, help='Configuration file path', required=True,action="store")
        parser_object.add_argument('--CREDENTIAL_PATH', type=str, help='Credential file path', required=True,action="store")
        parser_object.add_argument('--MY_INSTANCES', type=str, help='Instance port', required=True,action="store")
        parser_object.add_argument('--LOG', type=str, help='Log path', required=True,action="store")
        parser_object.add_argument('--TMP_FOLDER', type=str, help='Tmp folder', required=True,action="store")
        args_list = parser_object.parse_args()
        return args_list

    def get_instanceinfo(self,MY_INSTANCE_NAME):
        if MY_INSTANCE_NAME=="3306":
            credential_file=self.args_list.CREDENTIAL_PATH[0]
            conf_file=self.args_list.CONF_PATH[0]
        else:
            credential_file=self.args_list.CREDENTIAL_PATH[1]
            conf_file=self.args_list.CONF_PATH[1]
        return conf_file,credential_file

    def get_user_args(self,credential_file):
        user=commands.getoutput("grep user "+credential_file+" | grep -v ^# | head -n 1")
        password=commands.getoutput("grep password "+credential_file+" | grep -v ^# | head -n 1")
        host=commands.getoutput("grep host "+credential_file+" | grep -v ^# | head -n 1")
        user_args=" --"+user+" --"+host+" --"+password
        return user_args

    def get_args(self,conf_file,tmp_folder):
        args="--defaults-file="+conf_file+" --rsync --tmpdir="+tmp_folder+" --no-timestamp"
        return args

    def full_backup(self,args,user_args,backup_dir_full,date):
        print "Init backup..."
        stdout,stderr=Popen("sudo innobackupex "+args+" "+user_args+" "+backup_dir_full+"/"+date,shell=True, stdout=PIPE, stderr=PIPE).communicate()
        print "Preparing the backup for restore..."
        full_stdout,full_stdrr=Popen("sudo innobackupex --apply-log --redo-only "+backup_dir_full+"/"+date,shell=True, stdout=PIPE, stderr=PIPE).communicate()
        print "Backup done!"
        return full_stdout,full_stdrr

    def inc_backup(self):
        PASS

    def change_owner(self,backup_dir_full,date):
        owner_stdout,owner_stderr=Popen("sudo chown ncbackup:ncbackup -R "+backup_dir_full+"/"+date,shell=True, stdout=PIPE, stderr=PIPE).communicate()
        return owner_stdout,owner_stderr

    def compress(self,PREFIX_BACKUP,SCRIPT_PREFIX,backup_dir_full,date):
        print "Compress file"
        compress_stdout,compress_stderr=Popen("sudo tar czf "+PREFIX_BACKUP+"_"+SCRIPT_PREFIX+".tar.gz "+backup_dir_full+"/"+date+" --remove-files",shell=True, stdout=PIPE, stderr=PIPE).communicate()
        print "Compress Done."
        return compress_stdout,compress_stderr



def main():

    saveout = sys.stdout
    test=xtrabackup()
    sys.out=test.args_list.LOG

    for MY_INSTANCE_NAME in test.args_list.MY_INSTANCES.split(','):
        print "---- Processing instance: "+MY_INSTANCE_NAME+" ----"

        conf_file,credential_file=test.get_instanceinfo(MY_INSTANCE_NAME)

        user_args=test.get_user_args(credential_file)

        args=test.get_args(conf_file,test.args_list.TMP_FOLDER)

        full_stdout,full_stdrr=test.full_backup(args,user_args,test.backup_dir_full,test.date)

        owner_stdout,owner_stderr=test.change_owner(test.backup_dir_full,test.date)

        compress_stdout,compress_stderr=test.compress(test.PREFIX_BACKUP,test.SCRIPT_PREFIX,test.backup_dir_full,test.date)

    sys.stdout=saveout


if __name__ == "__main__":
    main()