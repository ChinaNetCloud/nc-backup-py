# nc-backup-py

## Introduction

nc-backup-py intends to be a comprehensive one stop solution for backups.

## Requirements
* Operating System
  * Linux
  * Windows (in development)

* Python >= 2.6 (Python 3 not supported)

## Quick Start

* Clone or Download the git repository and change directory .
  ```
  $ git clone https://github.com/ChinaNetCloud/nc-backup-py.git
  $ cd nc-backup-py
  ```

  or

  ```
  $ wget -O nc-backup-py.zip https://github.com/ChinaNetCloud/nc-backup-py/archive/master.zip
  $ unzip nc-backup-py.zip
  $ cd nc-backup-py-master
  ```

* Run setup
```
$ ./setup.py
```

* Edit configuration

* Execute Backup manually
```
$ python /path/to/backup.py -r -c /path/to/conf.json -l WARNING
```
* Optionally add a cronjob
```
$ crontab -e
00 03 * * * python /var/lib/nc-backup-py/backup.py -r -c /etc/nc-backup-py/conf.json
```

### Features

#### Features Available
* Backup to multiple clouds storages: AWS S3, Aliyun (Alibaba), Mounted writable drive.
* Compression, Encryption, Decryption, Split files
* Backup of regular files and Multiple Databases: MySQL Dump, Mongo DB dump, Postgres SQL dump.
* Send POST message reports to custom URL. Report includes Success, size, server, log, etc.
* Retry failed uploads and report messages.

#### Features Planned
* MySQL Xtrabackup
* Avoid multiple compreassion operations. This can actually be considered a bug.
* Optionally use or Not local drive to consolidate backup files (Direct Streaming to remote destination).
* SSH storage backup
* Send report messages using e-mail, sms, wechat
* Improve documentation.

#### Features under development
* ionice and network nice management.
* snapshots for different storages.
* clean up scripts for local and remote files.
* Windows Server compatibility
* Windows Server compatibility
* Active directory backup
* ms-sql backup.

#### Extending Features
* The solution accepts 2 ways to extend it:
  * Run custom separate program on any programming language,
  * Accept integrated plugins; this are Python special classes that can be understood by nc-backup-py.

In general nc-backup-py works similar to many backups systems but it's objetives are to achive could and linux servers backups. Let's get into it for you to start getting familiar with it.

Notice: If you are interested on leaning about the structure of the project go ahead and read the rest of the introduction, but you do not really need this information to be able to install the software. In that case you can jump straight to Quick setup; manual install (Quick Start Procedure) or installation instructions and try to follow them.

Let's start explaining with execution. The project has a main script that is executed by calling the following command:

`python /path/to/backup.py -r -c /path/to/conf.json -l WARNING`

This command is able to perform all the backup tasks in sequential order according to the conf/conf.json configuration file order. As you might have already noticed nc-backup-py is developed using python and the configuration file is a JSON file. One of the main ideas behind the new software is to decouple code from configuration completely, so if at some point you find that you have to modify code then there is a bug in the system and it needs to be taken care of, we appreciate if you report it as an issue.


#### How to contribute to the project and joing the team as volunteer:
We appreciate all controbutions and need and are looking forward for your help.

##### Developer:
1- Install the `test-dev` branch and get it to work.

2- Create an [Issue](https://github.com/ChinaNetCloud/nc-backup-py/issues) and start discussion providing as many details as possible, with maintainers team.

3- Once the isue is accepted you will be addred to the team as contributor, then you can start development.

4- Commit to your own branch.

5- Send merge request to test test-dev once done with your feature and update on Issues.

6- Iterate :P.

##### Use the product:
1- Download and install `master` branch,

2- Provide feedback on [Issue](https://github.com/ChinaNetCloud/nc-backup-py/issues) for suport,

3- If you think the project is useful or has potential, please add a star.


#### Edit the configuration file and change parameters**

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

Backup folder default folder is /opt/backup. Default installation folder is /var/lib/nc-backup-py. The configuration default will all be under /etc/nc-backup-py the permits on the files should be maintained the the ncbackup user will be made owner by default. All configuration files should be under this folders but if you know what you are doing, you can change. The longs will be in /var/log/nc-backup-py/nc-backup-py.log

### General other executable Scripts and improvements

All python modules are Optional and among others we have the following:
backup: Main script that can execute and control other scripts execution (needs arguments)
compression: compression script (needs arguments)
encryption Encryption and decryption script. (needs arguments)
filesbackup does backups of filesets with exclusions (needs arguments)
mysql_dump: MySQl backup.
(Optional) storage.py:AWS and OSS storage connects and saves files to different storages.
mongo
Postgres

## Plugins

We also have available a module/plugin feature in the configs available through configuration as well. current modules:
tools/size_calculation.py: Size calculation

### Tools also included

Every module or script include or make use of a set of tools included in tools folder. This scripts are supposed to be documented in details in the future, you do not need to to knw them to be able to install the software anyways.
date_str_utils.py
filesystem_handling
os_works
requests_utils
size calculation (This is also a plugin)

# Requirements

For now the system only supports python 2.6 and 2.7. You need to know the version of python where you are executing the script:

`~$ python

Python 2.7.5 (default, Nov 20 2015, 02:00:19)

[GCC 4.8.5 20150623 (Red Hat 4.8.5-4)] on linux2

Type "help", "copyright", "credits" or "license" for more information.

>>> exit()

~$`

### For AWS backups:

Install awscli:

`pip install awscli`

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

Then, edit the alioss config file.
`vim /etc/.alioss.conf ;`

Content:

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

Login Web page for Aliyun:

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

`2016-05-31 14:29:07,823 - ncbackup - INFO - Execution time in seconds: 4.38756585121
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

2016-05-31 14:30:30,214 - ncbackup - INFO - Execution time in seconds: 82.3907568455`

### Run

Create a cron job as follows:

`00 03 * * * python /path/to/executable -r -c /path/to/conf.json`

This will run the script with warning level and critical level logs stored only.
