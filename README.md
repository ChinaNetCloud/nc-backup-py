# nc-backup-py system installation

## Introduction:

This is the installation manual for nc-backup-py system currently in testing and development phase as wel as used for some productions systems. 

### Fetures
# NOTICE Need to add the features here

In general the new system works similar to the current ncbackup, but with some differences. Let's get into it for you to start getting familiar with it.
Notice: If you are interested on leaning about the structure of the project go ahead and read the rest of the introduction, but you do not really need this information to be able to install the software. In that case you can jump straight to Quick setup; manual install (Quick Start Procedure) or installation instructions and try to follow them.
Let's start explaining by the with execution. The project has a main script that is executed by calling the following command:

`python /path/to/backup.py -r -c /path/to/conf.json -l WARNING`

This command is able to perform all the backup tasks in sequential order according to the conf/conf.json configuration file order. As you might have already noticed the new system is developed using python and the configuration file is a JSON file. One of the main ideas behind the new software is to decouple code from configuration completely, so if at some point you find that you have to modify code then there is a bug in the system and it needs to be taken care of. So report it to abel.guzman at chinanetcloud.com and ops_backup at chinanetcloud.com.

## Skills

Understand basics about JSON format.
Linux commands
Is much easier if you understand BASICS of our current backups system but not a requirement.

## Quick setup (Quick Start Procedure)

This quick setup guide is to install ONLY our default filesbackup configuration (/etc /opt/ncscripts /var/spool/cron) and upload to AWS S3. Before you start, please make sure you have the requirements installed.

### Download the script to the server

let's use your home folder of a sudoer user as download folder:

`[abel.guzman@xxx] cd ~
[~]$ git clone https://gitlab.service.chinanetcloud.com/backup/nc-backup-py.git
`

### Use setup.py file to create user and other required tasks

Execute the file called setup.py in the nc-backup-py folder. This file executes automatically all the following tasks until configuration. The configuration will need to be done by you manually or using other method. To execute get in the git cloned directory and execute:
 
`# python setup.py`

This step should work correctly, if it does you can skip the following sub-section and go to "Edit the configuration file and change parameters":

#### Create user to run backup

Create basic folders structure and move files
To be sure it worked or not you just need to check the files en folder in the two steps to be at the right place and with the right permissions.

Create user to run backup:

`[~]$ sudo useradd -m ncbackup -s /sbin/nologin
[edit]Create basic folders structure and move files
[~]$ sudo mkdir /etc/nc-backup-py/`

Move the default configuration file from where the you downloaded to /etc/nc-backup-py/ and make ncbackup the owner e.g.:.

`[~]$ sudo mv ~/nc-backup-py/conf/* /etc/nc-backup-py/
[~]$ sudo chown ncbackup:ncbackup /etc/nc-backup-py/ -R`

Create log folder:

`[~]$ sudo  mkdir /var/log/nc-backup-py/
[~]$ sudo  chown ncbackup:ncbackup -R /var/log/nc-backup-py/`

Create code deployment directory, move code and make ncbackup the owner:

`[~]$ sudo mv ~/nc-backup-py/ /var/lib/
[~]$ sudo chown ncbackup:ncbackup -R /var/lib/nc-backup-py/`

Create default backup folder:

`[~]$ sudo mkdir /opt/backup/
[~]$ sudo chown ncbackup:ncbackup -R /opt/backup/`

### Edit the configuration file and change parameters**

If what you want to achieve is exactly the same as in this sample guide, you just need to edit the configuration file and change the server name to yours own server name:

`[~]$ sudo vim /etc/nc-backup-py/conf.json`

And then change:

`"HOSTNAME": "srv-nc-template-host-config",`

To:
 
`"HOSTNAME": "srv-your-hostname",`

Also make sure you have the right bucket in storage section so change this to the real bucket name:

`"BUCKET_NAME": "cnbackup"`
something like:

`"BUCKET_NAME": "realbucket"`

Here you can modify any other configuration wanted, but it will require for you to read the rest of the configs. depending on what you want specifically you might need to check other sections of the Configuration file specifications or the JSON file Reference manual.

### Run the job

Change to ncbackup user

`[~]$ sudo su - ncbackup -s /bin/bash
Last login: Mon Jul  4 09:31:49 UTC 2016 on pts/0
[~]$ whoami 
ncbackup
[~]$`

### Configure AWSCLI s3 access
You might also need to configure AWS credentials depending on the case,.

`[~]$ aws configure`

And follow instructions, you need only the ID Key, The secret key and the zone name. The rest of the parameters are optional.
In any case after configuration you should be able to do the following:

`[~]$ sudo su - ncbackup -s /bin/bash
Last login: Mon Jul  4 09:31:49 UTC 2016 on pts/0
[~]$ aws s3 ls
2016-04-18 06:35:27 xxx-bucket-name
(...)
2016-04-21 10:38:47 yyy-other-bucket-name
[~]$`

and run the following command:

`python /var/lib/nc-backup-py/backup.py -r -c /etc/nc-backup-py/conf.json`

To add it to cron you just need to add this line with crontab -e. Remember you need to edit ncbackup's cron file.

`00 03 * * * python /var/lib/nc-backup-py/backup.py -r -c /etc/nc-backup-py/conf.json`

And you are DONE! Your backups system should do the backups and send report to BRT.

### Decryption for servers with python 2.7

Download the files to /opt/backup e.g.:
`$ aws s3 cp s3://cnc-bj-backup/srv-nc-bj-zabbix-qa1/20160705_042923.tar.gz.crypt.000 /opt/backup
Execute the decryption command:
$ python /var/lib/nc-backup-py/encryption/encryption.py -d --KEY_FILE "/etc/nc-backup-py/key_file" --OBJECTIVES "/opt/backup/20160705_042923.tar.gz.crypt.000" --DESTINATION "/opt/backup/20160705_042923.tar.gz" --HOME_FOLDER "/var/lib/nc-backup-py"`

For more information on decryption, go to the decryption section

`Upgrading the system to the latest version`

The upgrade of the system might implicate changes of the config or not. If the upgrade does not require changes of the code yuo only need to download the new code from git and replace in /var/lib/nc-backup-py.

_Notice:_ You require upgrades when there are new changes committed to the git repository and for some reason you require those features or code.
Let's get to it, for that use the home folder of a sudoer user as download folder:

`[abel.guzman@xxx] cd ~
[~]$ git clone https://gitlab.service.chinanetcloud.com/backup/nc-backup-py.git`

Notice: You might need to clone a different branch for specific cases using -b <branch-name> statement e.g.:

`[~]$ git clone -b abel-dev https://gitlab.service.chinanetcloud.com/backup/nc-backup-py.git`

Now optionally you can remove the configurations from the script as is not required for most cases:

`rm -rf ~/nc-backup-py/conf`

Then move the code to /var/lib (The code folder), doing a backup first:

`cp -r /var/lib/nc-backup-py ~/nc-backup-py.DATE
rm -rf /var/lib/nc-backup-py
mv ~/nc-backup-py /var/lib`

Now you can test run the backup.

## Configuration standards

We have decided to change some of the parameters from the old ncbackup to the new nc-backup-py.

### Filesystem and locations

Backup folder should remain the same /opt/backup
Recommended location and our new standard is /var/lib/nc-backup-py
The configuration will all be under /etc/nc-backup-py the permits on the files should be maintained from the old system as well as the files standards. All configuration files should be under this folder.
The longs will be in /var/log/nc-backup-py/nc-backup-py.log
So make sure this folders exist and ncbackup is the owner:

### Executable Scripts and improvements

All python modules are Optional and among others we have the following:
backup: Main script that can execute and control other scripts execution (needs arguments)
compression: compression script (needs arguments)
encryption Encryption and decryption script. (needs arguments)
filesbackup does backups of filesets with exclusions (needs arguments)
mysql_dump: MySQl backup.
(Optional) storage.py:AWS and OSS storage connects and saves files to different storages.
mongo
Postgres

## New features:
Reporting improvements
Retries for AWS, OSS uploads and post reports.

## Pending Scripts:
snapshots for different storages.
clean up scripts for local and remote files.
Windows compatibility
Active directory backup
ms-sql backup.

## Road Map:
1- Optimize HDD Usage
2- File copy, DB Dump, Compression should be a single operation, i.e data should be piped from one to the other without temp files.
Streaming compressed, encrypted data to the cloud with a small local cache (No large locally stored encrypted files).
Implement incremental backups.
3- Improve Documentation


## Plugins

We also have available a module/plugin feature in the configs available through configuration as well. current modules:
tools/size_calculation.py: Size calculation

### Tools also included

every module or script include or make use of a set of tools included in tools folder. This scripts are supposed to be documented in details in the future, you do not need to to knw them to be able to install the software anyways.
date_str_utils.py
filesystem_handling
os_works
requests_utils
size calculation (This is also a plugin)

## Requirements

For now the system only supports python 2.6 and 2.7. You need to know the version of python where you are executing the script:
~$ python
Python 2.7.5 (default, Nov 20 2015, 02:00:19) 
[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2
Type "help", "copyright", "credits" or "license" for more information.
>>> exit()
~$ 

### For AWS backups:

Install awscli:
pip install awscli

### For Aliyun OSS

Install AliYun OSS tools
You might need to add aliyun repo first and then:

`# yum install aliyun-oss-tools`

Add x privilege to command

`# chmod a+x /usr/bin/alicmd`

Get help information

`# alicmd -h`

Check if this files exist (/etc/.alioss.conf), if does not exist, proceed with configure AliYun OSS, else (if exist), remove the old config file

`rm -rf /etc/.alioss.conf` 

Configure AliYun OSS

`# alicmd --config`

Then, edit the alioss config file. vim /etc/.alioss.conf ;
`[options]
retry_times = 15
multi-upload = on        # if the backup file size is more than 100MB
Warning: Before you configure, please make sure you check if this server can access aliyun OSS using private address. The difference is that if the server can access Aliyun using private address the traffic is considered internal therefore it's FREE. If you use public addresses the customer is charged for this traffic. this amount is changed as per daily bakup, so it could be a lot if there is a lot of information to backup.
You will see some contents like below
[INFO]: Start to config AliYun Open Storage Service.
[INFO]: Host 'storage.aliyun.com' selected automatically. You can also update file  /etc/alioss.conf manually. # Backup Host is determined automatically.
Please input your ACCESS_ID:       # FIND THE ID/KEY in our keepass file(search OSS).
Please input your ACCESS_KEY:
Please input your bucket:        #Our default bucket is "chinanetcloud"
Plase input CNC server name:            
[INFO]: AliYum OSS is configured sucessfully !
[INFO]: Configuration file saved.`

Verify OSS Configuration file:

`# alicmd --show
XXcloud 2012-06-19T07:05:33.000Z  # Should list all buckets we have`

Login Web page for Aliyun
`URL: www.aliyun.com (username and password) Selete 
用户中心 --> 管理控制台 --> 开放存储服务OSS --> OSS 管理 --> OSS体验站`
`
Check the backup files
`# alicmd -l`

### Testing Do not use in Production for now
Install OSS SKD:
`pip install OSS2`
python 2.7 or 2.6

### Python modules

Notice: This modules come installed with most versions of Red Hat based distributions, you can try to execute the backups systems and if they are not present then install manually. If the modules required are not present the wscript will fail and inform about the name of the required modules. You can use yum search for looking for the binary installers if wanted or pip to install them.
You might need to enable epel repo if not enabled to install some modules:

`$ wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
$ sudo rpm -iUvh epel-release-latest-6.noarch.rpm`

requests (could be installed with pip if not present: 'pip install requests' or using yum as well)
CentOS 7 and 6
`sudo yum install python-requests.noarch`
Crypto (Only for python 2.7)
CentOS 7
`sudo yum install python-crypto.x86_64`
CentOS 6
`sudo yum install python-crypto2.6.x86_64`
argparse
simplejson (Only for python 2.6)
`$ sudo yum install python-simplejson.x86_64`
backport_collections (Only for python 2.6)
`pip install backport_collections`

Aliyun documentation here in chinese: https://help.aliyun.com/document_detail/32026.html?spm=5176.doc32027.6.296.03bgw0

### Other requirements (Optionals)
This are required if you need to install some of the dependencies, but they are not requirements of the software.
git
pip
Installing pip on centOS 6.
$ sudo yum install python-pip

##Installation

Notice: Check that you have the requirements installed (Check the requirements section) on the server.
### Check that the user ncbackup exists
Check that the user ncbackup exists and is the owner of the work folder as well as it can read the rest. You will have to create a dedicated user (eg. ncbackup).
Notice: The script does not work as 'root'
`# useradd -m ncbackup -s /sbin/nologin`
### Clone repository:
git clone -b master https://gitlab.service.chinanetcloud.com/backup/nc-backup-py.git
Call (cd) into the folder:
cd nc-backup-py
### Configure JSON
Follow the guide lines in the chapter called The JSON config file. The confign file is in conf/conf.json, but you can create your own with a custom name if wanted. The configuration can be anywhere, but out new standard is going to be inside /etc.
### Configure credentails accordingly
If MySQL Db server, create credentials file, create encription key, etc.
You need to create a MySQL user that can perform the dump of the database.
Connect to mysql:
CREATE USER 'ncbackupdb'@'localhost' identified by 'PASSWORD';
GRANT SELECT, RELOAD, SHOW DATABASES, LOCK TABLES, REPLICATION CLIENT, SHOW VIEW, EVENT ON *.* TO 'ncbackupdb'@'localhost';
flush privileges;
localhost host only apply for local backup -- if you need to connect to a remote database, you will need to adapt accordingly (replace 'localhost' by '%')
Create MySQL login / pass file :
`# vim /etc/nc-backup-py/mysql_backup.creds
[mysqldump]
user=ncbackupdb
password=PASSWORD
host=localhost
socket=/var/lib/mysql/mysql.sock 

[mysql]
user=ncbackupdb
password=PASSWORD
host=localhost
socket=/var/lib/mysql/mysql.sock`
Notice: For mysql backups to work on Unbuntu and maybe other distrobutions but CentOS6, 7 AMI Linux, etc. you need to make sure the MySQL is readable by ncbackup. The best way to do this is to add ncbackup to mysql group and then make sure the group has read access.
####Create log directory
No need to create the file, but you need to specify the path to the file in the configs). This needs to be fixed. E.g.:
mkdir /var/log/nc-backup
Notice: This should be the same path as in the JSON config file.
#### Add sudo options
The ncbackup user needs to be able to run some privileged commands.
edit sudoers
`# visudo
add the following to sudoers configurations. Could be here: /etc/sodoers:
Cmnd_Alias NCBACKUP = /bin/tar czCf / [A-z_/ ]*, /bin/tar czf [A-z_/ ]*
ncbackup ALL = NOPASSWD: NCBACKUP
Defaults:ncbackup   !requiretty`
#### Run
python /path/to/backup.py -r -c /path/to/conf.json
Notice: You might need to put the whole file path to backup.py and conf.json
#### The logs
The logs are vey useful for troubleshooting purposes. Let's take a look:
2016-05-31 14:29:07,823 - ncbackup - INFO - Execution time in seconds: 4.38756585121
2016-05-31 14:29:07,823 - ncbackup - INFO - Section 8: STORAGE_OSS.
2016-05-31 14:29:07,823 - ncbackup - INFO - Loading executable module: storage
2016-05-31 14:29:07,824 - ncbackup - INFO - Automatically selected python as execution method
2016-05-31 14:29:07,824 - ncbackup - INFO - Preraring for execution as follows: python /Users/cncuser/Documents/py/nc-backup-py/storage/storage.py
2016-05-31 14:29:07,824 - ncbackup - INFO - Prapare execution finised script. Now prepare parameters to pass is going to be executed
2016-05-31 14:29:07,824 - ncbackup - INFO - Module specific parameters iteration: --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" 
2016-05-31 14:29:07,824 - ncbackup - INFO - Module specific parameters iteration: --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" 
2016-05-31 14:29:07,824 - ncbackup - INFO - Module specific parameters iteration: --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" 
2016-05-31 14:29:07,824 - ncbackup - INFO - Module specific parameters iteration: --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" --ALIYUN_CREDENTIALS "/etc/.alioss.conf" 
2016-05-31 14:29:07,824 - ncbackup - INFO - Module specific parameters iteration: --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" --ALIYUN_CREDENTIALS "/etc/.alioss.conf" --REMOVE_OBJECTIVES "True" 
2016-05-31 14:29:07,824 - ncbackup - INFO - General parameters iteration: --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" --ALIYUN_CREDENTIALS "/etc/.alioss.conf" --REMOVE_OBJECTIVES "True" --HOSTNAME "srv-nc-py27-abel-mac-db1" --WORK_FOLDER "/Users/cncuser/Downloads/backup" --LOCAL_BACKUP "/Users/cncuser/Downloads/backup/local" --HOME_FOLDER "/Users/cncuser/Documents/py/nc-backup-py" --LOG_FOLDER "/Users/cncuser/Documents/py/nc-backup-py/log/ncbackup.log" 
2016-05-31 14:29:07,824 - ncbackup - INFO - Finished parameters preparation for section
2016-05-31 14:29:07,824 - ncbackup - INFO - Calling module: python /Users/cncuser/Documents/py/nc-backup-py/storage/storage.py --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" --ALIYUN_CREDENTIALS "/etc/.alioss.conf" --REMOVE_OBJECTIVES "True" --HOSTNAME "srv-nc-py27-abel-mac-db1" --WORK_FOLDER "/Users/cncuser/Downloads/backup" --LOCAL_BACKUP "/Users/cncuser/Downloads/backup/local" --HOME_FOLDER "/Users/cncuser/Documents/py/nc-backup-py" --LOG_FOLDER "/Users/cncuser/Documents/py/nc-backup-py/log/ncbackup.log" 
2016-05-31 14:29:07,824 - ncbackup - INFO - List of parameters passed to script: python /Users/cncuser/Documents/py/nc-backup-py/storage/storage.py --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" --ALIYUN_CREDENTIALS "/etc/.alioss.conf" --REMOVE_OBJECTIVES "True" --HOSTNAME "srv-nc-py27-abel-mac-db1" --WORK_FOLDER "/Users/cncuser/Downloads/backup" --LOCAL_BACKUP "/Users/cncuser/Downloads/backup/local" --HOME_FOLDER "/Users/cncuser/Documents/py/nc-backup-py" --LOG_FOLDER "/Users/cncuser/Documents/py/nc-backup-py/log/ncbackup.log" 
2016-05-31 14:29:07,825 - ncbackup - INFO - Executing system the system external command: python /Users/cncuser/Documents/py/nc-backup-py/storage/storage.py --OBJECTIVES "/Users/cncuser/Downloads/backup/encrypted" --DESTINATION "oss" --BUCKET_NAME "cncbackup" --ALIYUN_CREDENTIALS "/etc/.alioss.conf" --REMOVE_OBJECTIVES "True" --HOSTNAME "srv-nc-py27-abel-mac-db1" --WORK_FOLDER "/Users/cncuser/Downloads/backup" --LOCAL_BACKUP "/Users/cncuser/Downloads/backup/local" --HOME_FOLDER "/Users/cncuser/Documents/py/nc-backup-py" --LOG_FOLDER "/Users/cncuser/Documents/py/nc-backup-py/log/ncbackup.log" 
2016-05-31 14:30:30,214 - ncbackup - INFO - the execution was succesfull
2016-05-31 14:30:30,214 - ncbackup - INFO - StdOut: Executing backup files type: oss
calling OSS storage upload functions
Trying uploading to Aliyun OSS bucket: cncbackup
Now we read the Aliyun credentials from the file: /etc/.alioss.conf
/etc/.alioss.conf
Upload attempt 1 successful.
Attempt failed
Upload attempt number: 1 FAILED for: /Users/cncuser/Downloads/backup/encrypted/20160531_142903.tar.gz.crypt.001

We will wait for: 1 minute(s) before upload attempt number: 2
Upload attempt 2 successful.
Executing system the system external command: rm -rf /Users/cncuser/Downloads/backup/encrypted
[(0, 'Status: 200 Request ID: 574D2F34727EC395763E7B2BC5744FE5A7186F0175DEB0440B22619E', ''), (0, 'Status: 200 Request ID: 574D2F853DD1246111751CFD50140945BA676D8F7A0FC0B5D4F3F3A1', ''), (0, '', 'stderr: ')]

2016-05-31 14:30:30,214 - ncbackup - INFO - Execution time in seconds: 82.3907568455
## Configuration

### The JSON config file

#### Introduction
A .json config file is the sole config for all modules and scripts used. This is standard JSON; with a few Keywords specific to the software and sections. Maybe at some point in the future we might need to implement being able to have more than one .json config file that can be included from a central file. Something like and include feature. The config only has one mandatory section It looks like this:
    {
      "GENERAL": {
        "HOSTNAME": "WIN-G5AKB09AALD",
        "WORK_FOLDER": "c:\\backup",
        "LOCAL_BACKUP": "c:\\backup\\local",
        "HOME_FOLDER": "c:\\backup\\nc-backup-py",
        "LOG_FOLDER": "c:\\backup\\nc-backup-py\\log\\ncbackup.log",
        "DISK_SPACE_CHECK": "False",
        "DISK_SPACE_THRESHOLD": "20"
        },
    (...)
    }
#### The GENERAL section
Basics of the .json file:
HOSTNAME: is the China Net Cloud hostname e.g. srv-nc-zabbix-db1, it can actually be any name, but we should keep it like that to follow out standards.
WORK_FOLDER: is a tmp folder that the system uses for temporary storage of files. This folder in some cases might at least need 2x the size of the backup of available space.
HOME_FOLDER: Where the backups software installation files live
(Optional) LOCAL_BACKUP: if the server needs to keep local backups, this is the folder where they will be kept.
LOG_FOLDER: Folder or to store logs or specific file name where to store the logs.
DISK_SPACE_CHECK: is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
DISK_SPACE_THRESHOLD: Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%.
#### General tips to keep present:

Every section is flexible to add as many parameters as the specific module to be execute needs.
The only section with a compulsory name is GENERAL, because it has parameters that are used by all the other modules. The rest of the executable modules can be called any name, as long a you use a few key words (from 0 to 3 depending on how special the module is; development language, path, executable name) that explain how to find and execute.
The config file is the same for windows and Linux, what changes is the OS specific parameters.
The size should be a number integer that represents the MB size of one split part.
The file paths supplied to the different sections can be in any of the POSIX formats as absolute paths, relative paths, etc. The path ending in / or not should not cause problems to the diferent scripts and if it does a bug case should be opened.
We are working now on making the system also able to work with windows paths, but this is still a work in progress
The comma (,) at the end of a line means there is a sibling instruction after the one your are working on. This is JSON standard.
Keep present that all the parameters from configuration section of the plugins are passed to the class as a python dictionary when pass parameter to the class when costructed. So it's your duty to parse this dictionary if you need config parameters.
The credentials, configs and keyfiles is advisable to be added to /etc instead of the current paths, this are just testing and development paths that are used currently for development. The script should be flexible engouh to have the configs anywhere. The specific standard is to be still agreed on.
#### Files backup section

The following is a real working section that calls and executes external colde to compress a fileset.
     "FILESET":{
       "ACTION": "execute",
       "NAME": "filesbackup",
       "EXECUTE_WITH": "python",
       "EXECUTABLE": "",
       "PARAMETERS": {
         "FILESET_INCLUDE": "/etc /opt/ncscripts /var/spool/cron",
         "FILESET_EXCLUDE": ""
       }
     }
Notice: FILESET_INCLUDE can not be "/"
##### Optional parameters
This section as most of the others have most of it's parameters as optional. For a default Cent OS 6 or 7 configuration this section should work the same as the section before as it would assume default configurations according to our new standards.
     "FILESET":{
        "ACTION": "execute",
        "NAME": "filesbackup"
     }
##### Line by line explanation
"FILESET":{ Defines a section beginning, the name can be anything, but as a convention is good to give it a name according to it's content.
"ACTION": "execute", The kay word ACTION says to the script the now I want to say what to do in the section, there are 2 possible options defined for now:
execute: means an external code script is going to be executed.
load: a dynamic module will be loaded. There is a slide but important difference between "execute" and "load", load is to execute native python code in the for of dynamic imports while the other executes external independent scripts that can be done using any programming language as long as it follows some basic rules.
"NAME": "filesbackup", NAME is to specify the name of the folder where to find the plugin or script to load/execute. Is advised to call the modules the same name of the folder, but is not a requirement. Then "filesbackup" is the name of the external script to be executed in this case.
(Optional) "EXECUTE_WITH": "python", Is to know what type of code you need to execute, if your code is python, then you do not need to specify.
(Optional) "EXECUTABLE": "", is to know which one is the executable file in the module.
(Optional) "PARAMETERS": { This subsection is to pass parameters to the module to be executed/loaded. Inside you add parameters that you want the plugin/script to receive.
(Optional, specific to the plugin or script to load or execute) "FILESET_INCLUDE": "/etc /Users/cncuser/Documents/", The parameters are all depending on what you need to execute your code. Every section can have different parameters depending on the way it was programmed.
##### The plugins
Plugins also need a config section similar to this:
     "SIZE":{
       "ACTION": "load",
       "FROM": "tools",
       "FILENAME": "size_calculation",
       "CLASS": "SizeCalculation",
       "PARAMETERS": {
         "TARGETS": "/Users/cncuser/Downloads/backup/encrypted"
       }
     }
This is a working plugin that only calculates the size of the files to be backed up.
#### Sections and modules specifics

#### MySQL Dump:
  `"MYSQL": {
    "ACTION": "execute",
    "NAME": "mysql_backup",
    "EXECUTABLE": "mysql_dump.py",
    "EXECUTE_WITH": "python",
    "PARAMETERS": {
      "CREDENTIAL_PATH": "/etc/nc-backup-py/mysql_backup.creds",
      "DATA_DIR": "/var/lib/mysql/data",
      "MY_INSTANCES": "3306",
      "BINLOG_PATH": "/var/lib/mysql/data",
      "BINLOG_FILE_PREFIX": "mysql-bin",
      "DESTINATION": "/opt/backup",
      "TAR_COMMAND": "sudo /bin/tar czf",
      "MYSQL_DUMP_BINARY": "/usr/bin/mysqldump",
      "MYSQL_BINARY": "/usr/bin/mysql",
      "PREFIX_FOLDER": "mydump",
      "EXCLUDE_DB": "",
      "BINLOG_DAYS": "3",
      "EXCLUDE_TABLE": "mysql.user mysql.func mysql.event"
    }
  }`
This section executes a external script that executes a dump on the MySQL DB. Some parameters implementations are still pending or not completed.
#### Mongo DB
  "MONGODB":{
    "ACTION": "load",
    "FROM": "mongo",
    "FILENAME": "mongo",
    "CLASS": "MongoBackup",
    "PARAMETERS":{
      "MONGO_USER": "",
      "MONGO_PWD": "",
      "MONGO_HOST": "127.0.0.1",
      "MONGODUMP_BIN": "/usr/bin/mongodump",
      "TAR_COMMAND": "sudo /bin/tar czf",
      "PREFIX_FOLDER": "mongodump",
      "DESTINATION": "/opt/backup"
    }
  }
Notice: This is a plugin instead of an executable independent script.
#### Postgresql
Create backup user ncbackup in postgresql
postgres=> create user ncbackup with password 'PASSWORD';
Details about how to create user in pgsql, please refer to Basic postgresql management procedure
Grant select privilege on all user_created tables to ncbackup
Customerdb=> grant select on $TABLE_NAME to ncbackup;
You have to grant privilege one by one, of cource, you could also create a batch scipt to do it.
Create .pgpass file in /home/ncbackup with following contents, that is for backup script authenticaiton.
localhost:*:*:ncbackup:$PASSWORD
You should change the $PASSWORD part accordingly
Setup ownership and privilge like the following:
[root@srv-xxx-xxx ~]# ls -l /home/ncbackup/.pgpass 
-rw------- 1 ncbackup ncbackup 34 Jun 12 17:04 /home/ncbackup/.pgpass
[root@srv-xxx-xxx ~]# 
Be careful, 600 privilege is a must
when the backup will be restored, before you do anything, you must create all the user and database related to the backup, or the restore will fail
##### Config file
  `"POSTGRES":{
    "ACTION": "load",
    "FROM": "postgres",
    "FILENAME": "postgres",
    "CLASS": "PostgresBackup",
    "PARAMETERS": {
      "PREFIX_FOLDER": "pgdump",
      "PSQLDUMP": "/usr/bin/pg_dump",
      "PSQL": "/usr/bin/psql",
      "DESTINATION": "/opt/backup",
      "EXCLUDE_DB": ""
    }
  }`
Notice: This is a plugin instead of an executable independent script.
Notice: The script can exclude databases with EXCLUDE_DB, but is can not exclude tables yet.
#### Compression
  `"COMPRESSION": {
    "ACTION": "execute",
    "NAME": "compression",
    "EXECUTABLE": "",
    "EXECUTE_WITH": "",
    "PARAMETERS": {
      "TAR_COMMAND": "sudo /bin/tar czCf /",
      "TARGETS": "/opt/backup/files /opt/backup/mongodump",
      "DESTINATION": "/opt/backup/compressed",
      "REMOVE_TARGETS": "True"
    }
  }`
  
This section takes a set of folders and compresses them. The parameters "REMOVE_TARGETS": "True" means that the script will remove the fileset passed as parameters. We are discussing the possibility of changing "OBJECTIVES" in all sections to some other candidate word like FILESETS. If this change is finally implemented the development changes are not a lot. Compression also has many optional parameters, so in a standard CentOS 6 or 7 configuration this configuration could look like this:
  `"COMPRESSION": {
    "ACTION": "execute",
    "NAME": "compression",
    "PARAMETERS": {
      "TARGETS": "/opt/backup/files /opt/backup/mongodump"
    }
  }`
  
The system will assume on it's own the default values as per the first compression configuration sample. You only need to change it if your parameters NEED to be different, even when we would not advise it unless strictly required.
#### Encryption
  `"ENCRYPTION": {
    "ACTION": "execute",
    "NAME": "encryption",
    "PARAMETERS": {
      "KEY_FILE": "/etc/nc-backup-py/key_file",
      "FILE_SIZE": "100",
      "TARGETS": "/opt/backup/compressed",
      "DESTINATION":"/opt/backup/encrypted",
      "REMOVE_TARGETS": "True"
    }
  }`
This section as the name indicates encrypts files, but also splits long files according to FILE_SIZE give in MB. "KEY_FILE" is the path to the key file.
Regarding the optional end required parameters the same could be exported to the encryption configuration so the minimal working configuration for a standard system is as follows:
  `"ENCRYPTION": {
    "ACTION": "execute",
    "NAME": "encryption"
  }`
Notice: Out standard for the configurations has changed so now all the configuration files have to be in /etc/nc-backup-py/ in this case the key file will be in /etc/nc-backup-py/key_file.
#### Storage
#####Local backup
  `"STORAGE_LOCAL": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"local",
      "TARGETS": "/opt/backup/encrypted"
    }
  }`
##### AWS s3
  `"STORAGE": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "TARGETS": "/opt/backup/encrypted",
      "DESTINATION":"s3",
      "BUCKET_NAME": "cncbackup",
      "UPLOAD_COMMAND": "aws s3 cp",
      "REMOVE_TARGETS": "True"
    }
  }`
This section is to store the backup, in this case s3. S3 is the only current backend implemented, but the script is supposed to support various backends including OSS, SSH, etc.
##### Aliyun OSS
  `"STORAGE_OSS": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "TARGETS": "/Users/cncuser/Downloads/backup/encrypted",
      "DESTINATION":"oss",
      "BUCKET_NAME": "cncbackup",
      "ALIYUN_CREDENTIALS": "/etc/.alioss.conf",
      "REMOVE_TARGETS": "True"
    }
  }`
##### Combine storages
  `"STORAGE_LOCAL": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"local",
      "TARGETS": "/opt/backup/encrypted"
    }
  },
  "STORAGE": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"s3",
      "BUCKET_NAME": "bucketname",
      "TARGETS": "/opt/backup/local",
      "REMOVE_TARGETS": "False"
    }
  }`
##### QA
 `"QA":{
   "ACTION": "load",
   "FROM": "qa",
   "FILENAME": "qa",
   "CLASS": "QA"
 }`
This feature is still under development in test conceptual phase, the idea is for the script to be able to detect the problems on it's own and at some point even auto-fix them. For now it's just included as a proof of concept module it only checks that the user running the script is ncbackup and logs a warning if the user is wrong. Please provide feedback on the things that the script is supposed to QA for so the development can be carried out following the best and more useful practices.
#### AWS CLI integration

Q: Does the AWS CLI validate checksums?
The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios. Upload The AWS CLI will calculate and auto-populate the Content-MD5 header for both standard and multipart uploads. If the checksum that S3 calculates does not match the Content-MD5 provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See aws help returncodes for more information. Taken from AWS CLI FAQ
## How to decrypt

###if the server doing backups has python 2.7

The encryption script is the same script used for decription. Is should be user as follows:

`python encryption/encryption.py -d --KEY_FILE "conf/key_file" --OBJECTIVES "/path/to/file/name" --DESTINATION "/path/where/the/resulting/will/be" --HOME_FOLDER "/path/to/nc-backup-py"`

-d: is to say we are decrypting.
--KEY_FILE "conf/key_file": is to indicate the path to the keyfile to used for decryption.
--OBJECTIVES "/path/to/file(s)": It's to say where are the encrypted files to be decrypted. if the download is more than one file they need to have names that start with the same partern; the software asumes you mean wild card (*) at the end. In other words, the names should be like something like this filename.tar.gz.crypt.000, filename.tar.gz.crypt.001, filename.tar.gz.crypt.00N, so in this case yout path should contanin the common part's of the name "filename.tar.gz.crypt.00".
--DESTINATION "path/and/name/of/tar.gz/file": this is the name and path that you want the resulting file to have after decryption
--HOME_FOLDER "/path/to/source/code/nc-backup-py": this is for the encryption script to know where the whole backups software is installed.

Example for a single file:

`python /var/lib/nc-backup-py/encryption/encryption.py -d --KEY_FILE "/etc/nc-backup-py/key_file" --OBJECTIVES "/opt/backup/20160705_042923.tar.gz.crypt.000" --DESTINATION "/opt/backup/20160705_042923.tar.gz" --HOME_FOLDER "/var/lib/nc-backup-py"`

Example for multiple files:
`python /vagrant/nc-backup-py/encryption/encryption.py -d --KEY_FILE "/vagrant/nc-backup-py/conf/key_file" --OBJECTIVES "/opt/backup/20160607_161750.tar.gz.crypt.00" --DESTINATION "/opt/backup/20160607_161750.tar.gz" --HOME_FOLDER "/vagrant/nc-backup-py"`

Notice: The only difference to decrypt one or more than one file is in the name of --OBJECTIVES. The first example show the whole path and the second example shows only the path with the part of the name that is common.

After this you have to untar the file using something like this:

`tar -xvf /opt/backup/20160607_161750.tar.gz /opt/backup/`
Idea: We might want develop a feature in the near future called "restore" that would do all the work for you and give you back the files already decompressed. This feature could even log information to BRT about the Restore job, and use dates, etc

### if the server doing backups has python 2.6

# NOTICE: Add MATERIS
Use the same method as weth ncbackup bash script: https://wiki.service.chinanetcloud.com/wiki/Operations:NC-OP_TP-782-How_to_restore_GPG_encrypt_backup_files

### Reference Manual the JSON file:

## General section

GENERAL - Identifies the main section of the configuration. The content of this section is passed to most scripts and plugins executed.
HOSTNAME - Server unique identificator name.
WORK_FOLDER - Temporary folder to do the works.
LOCAL_BACKUP - Place to keep the copies of local backups if this option is selected. This will be probably deprecated in firther versions of the software.
HOME_FOLDER - Place where the source code is located (Install folder).
LOG_FOLDER - Path to log file, this variable will be modified in the next version of the software.
DISK_SPACE_CHECK: is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
DISK_SPACE_THRESHOLD: Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%. This value determines how to react to HDD getting full. if you set it to 20% then you will get a warning if the HDD space is less than 20%. If the space goes under half the threshold (20% in this case, so 10%) so instead of a warning you will get a Critical or Error instead. Now if the space left goes under 10 times lower than the threshold (in the case of 20% it will be 2%), then the backup system will stop execution immediately and send a failure report.
[edit] Sections and key words

ACTION - tells the software what to do with the section of the configuration. for now it has 2 options that actually do something. In other words how to loadthe code. Execute and load, find theit entries for explanations of what they do.
execute - Key word for the ACTION parameter, execute means that this section executes and external script that is not dependant on the main script and needs it's own way to be executed.
load - Key word for the ACTION parameter, load means that this section loads a pluging via importing it dynamically. the code doe not depend on each other but the dynamically loaded code has to follow certain structure.
NAME Name of and external script to execute. the software is going to look for a folder called the name spacified in this parameter
FROM - folder where the plugin is located. This parameter might be merged with NAME in future versions.
EXECUTABLE- Optional parameter to say the name of the executable script inside the folder called NAME. This parameter needs to be specified only if the external script is not python or if the external script's name if different from the folder where it is. So the default value is the same as NAME parameter if not specified.
EXECUTE_WITH - Optional parameter to say what software to use to execute. The software is able to execute any type of scripts; bash, php, perl, python, the default value is python if not specified.
PARAMETERS- Optional paramter to specify parameters to pass to the script ot plugin.
TAR_COMMAND- Optimal parameters, to execute tar command on custom systems. the default calue is normally 'sudo /bin/tar czCf /' if not specified. this parameter can be specified in the following sections: FILESET, DBSBACKUP, COMPRESSION
TARGETS or OBJECTIVES- This parameter is to specify a group of targets to work with, is used by most scripts and plugins. We are in a discussion to probably will completely remove OBJECTIVES in the near futire, please do not use it for configurations anymore.
DESTINATION- Where to store the results. Used by most modules.
REMOVE_TARGETS / REMOVE_OBJECTIVES - If you want to remove the Target (OBJECTIVES) files or not. it accepts two possible values; True or False. The default value is True. REMOVE_OBJECTIVES will be deprecated in later versions in favor of REMOVE_TARGETS.
True - Yes
False - Not, No
KEY_FILE - parameter used by the encryption and decryption script as key. this parameter should contain the path to a key file, normally in /etc.
FILE_SIZE - Size of the encrypted files, always given in MB. The next versions might include other units if deamed required.
[edit]MYSQL Specifics:
CREDENTIAL_PATH - This is to specify the path to the MySQL credentials file. We will consider using the same Variable Name for other database systems.
CONF_PATH - This if for the path to MySQL my.cnf file (config file normally here /etc/my.cnf).
DATA_DIR - MySQL data dir, the company normally uses /var/lib/mysql/data
MY_INSTANCES - List space separated ports for the different instances running on a server default: "3306",
BINLOG_PATH - Path to binary logs for MySQL.
BINLOG_FILE_PREFIX - this is the beginning of the name normally defined my.cnf
MYSQL_DUMP_BINARY - Path to mysqlgdump binary executable file.
MYSQL_BINARY - Path to MySQL binary executable file.
PREFIX_FOLDER - Name of the folder and file prefix for MySQL backups inside the WORK_FOLDER.
EXCLUDE_DB - Database name to exclude.
EXCLUDE_TABLE Database and table names to exclude separated by a "." follow standard SQL notation e.g.: "mysql.user mysql.func mysql.event"
BINLOG_DAYS - Number of days of bin-logs to take.

#### Other MySQL instructions to be documented


  "MONGODB":{
    "ACTION": "load",
    "FROM": "mongo",
    "FILENAME": "mongo",
    "CLASS": "MongoBackup",
    "PARAMETERS":{
      "MONGO_USER": "",
      "MONGO_PWD": "",
      "MONGO_HOST": "127.0.0.1",
      "MONGODUMP_BIN": "/usr/bin/mongodump",
      "TAR_COMMAND": "sudo /bin/tar czf",
      "PREFIX_FOLDER": "mongodump",
      "DESTINATION": "/opt/backup"
    }
  },
  "POSTGRES":{
    "ACTION": "load",
    "FROM": "postgres",
    "FILENAME": "postgres",
    "CLASS": "PostgresBackup",
    "PARAMETERS": {
      "PREFIX_FOLDER": "pgdump",
      "PSQLDUMP": "/usr/bin/pg_dump",
      "PSQL": "/usr/bin/psql",
      "DESTINATION": "/opt/backup",
      "EXCLUDE_DB": ""
    }
  }
### Run

Create a cron job as follows:
00 03 * * * python /path/to/executable -r -c /path/to/conf.json
This will run the script with warning level and critical level logs stored only.

### Known issues 

#### ssl issues on python 2.6

You get the following warning:
/usr/lib/python2.6/site-packages/pip/_vendor/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
 InsecurePlatformWarning
Please ignore this message; the software works just fine, this is a problem with a deprecated ssl python library.

#### gpg-agent --daemon on python 2.6
If you see this error below:
"can’t connect to `/home/user/.gnupg/S.gpg-agent’: No such file or directory"

Then launch gpg agent daemon:

`$ gpg-agent --daemon
GPG_AGENT_INFO=/tmp/gpg-Y1AjlZ/S.gpg-agent:2523:1; export GPG_AGENT_INFO;
then you’ll just have to create a symbolic link:
$ cp -fs /tmp/gpg-Y1AjlZ/S.gpg-agent ~/.gnupg/`


## Contents

[1 Introduction](#test)

1.1 Skills

1.2 Quick setup (Quick Start Procedure)

1.2.1 Download the script to the server

1.2.2 Use setup.py file to create user and other required tasks

1.2.3 Create user to run backup

1.2.4 Create basic folders structure and move files

1.2.5 Edit the configuration file and change parameters

1.2.6 Run the job

1.2.7 Configure AWS

1.2.8 Decryption for servers with python 2.7

1.2.9 Upgrading the system to the latest version

2 New configuration standards

2.1 Filesystem and locations

2.2 Executable Scripts and improvements

2.2.1 New features:

2.2.2 Pending Scripts:

2.2.3 Road Map:

2.3 Plugins

2.4 Tools also included

3 Purpose

4 Requirements

4.1 For AWS backups:

4.2 For Aliyun OSS

4.2.1 Testing Do not use for now

4.3 Python modules

4.3.1 Other requirements (Optionals)

5 Installation

5.1 Check that the user ncbackup exists

5.2 Clone repository:

5.3 Configure JSON

5.4 Configure credentails accordingly

5.5 Create log directory

5.6 Add sudo options

5.7 Run

5.8 The logs

6 Configuration

6.1 The JSON config file

6.1.1 Introduction

6.1.2 The GENERAL section

6.2 General tips to keep present:

6.3 Files backup section

6.3.1 Optional parameters

6.3.2 Line by line explanation

6.3.2.1 The plugins

6.4 Sections and modules specifics

6.4.1 MySQL Dump:

6.4.2 Mongo DB

6.4.3 Postgresql

6.4.3.1 Config file

6.4.4 Compression

6.4.5 Encryption

6.4.6 Storage

6.4.6.1 Local backup

6.4.6.2 AWS s3

6.4.6.3 Aliyun OSS

6.4.6.4 Combine storages

6.4.7 QA

6.5 AWS CLI integration

7 How to decrypt

7.1 if the server doing backups has python 2.7

7.2 if the server doing backups has python 2.6

8 Reference Manual the JSON file:

8.1 General section

8.2 Sections and key words

8.2.1 MYSQL Specifics:

8.2.1.1 Other MySQL instructions to be documented

8.3 Run

8.4 Known issues

8.4.1 ssl issues on python 2.6

8.4.2 gpg-agent --daemon on python 2.6