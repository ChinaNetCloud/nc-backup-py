# Project nc-backup-py.

The project has a main script that is executed by calling the following command:

$ python backup.py -r -c /path/to/conf.json
this command is able to perform all the backup tasks in sequential order according to the conf.json configuration file order.

## Executable Scripts:
+ backup.py: Main script that can execute and control other scripts execution (needs arguments)
+ compression.py: compression script (needs arguments)
+ encryption.py Encryption and decryption script. (needs arguments)
+ filesbackup.py does backups of filesets with exclusions (needs arguments)
+ storage.py connects and saves files to different storages (done local and AWS S3). (needs arguments)
+ MySQl backup.

## Pending Scripts:

+ mongo
+ reporting
+ OSS storage
+ snapshots for different storages.
+ clean up scripts for local and remote files.
+ Windows compatibility
+ Active directory backup
+ ms-sql backup.

## Plugins
-We also have available a module/plugin feature in the configs available through configuration as well. current modules:
+ tools/size_calculation.py: Size calculation

## Tools
every module or script include or make use of a set of tools included in tools folder.
+ date_str_utils.py
+ filesystem_handling
+ os_works
+ requests_utils
+ size calculation (This is also a module)

## Requirements:
python 2.7

### Python modules
+ requests
+ Crypto (Actually Crypto.Cipher)

#### python 2.6 also requires:
+ argparse

## ROAD MAP:

To be added.

# The JSON config file.
## Introduction
A .json config file is the sole config for all modules and scripts used. This is standard JSON; with a few Keywords specific to the software and sections. Maybe at some point in the future we might need to implement being able to have more than one .json config file that can be included from a central file. Something like and include feature.
The config only has one mandatory section It looks like this:

    {
      "GENERAL": {
        "HOSTNAME": "WIN-G5AKB09AALD",
        "WORK_FOLDER": "c:\\backup",
        "LOCAL_BACKUP": "c:\\backup\\local",
        "HOME_FOLDER": "c:\\backup\\nc-backup-py",
        "LOG_FOLDER": "c:\\backup\\nc-backup-py\\log\\ncbackup.log"
        },
    (...)
    }

## Legend of the GENERAL section and other general basic understanding of the .json file:
+ HOSTNAME: is the China Net Cloud hostname e.g. srv-nc-zabbix-db1, it can actually be any name, but we should keep it like that to follow out standards.
+ WORK_FOLDER: is a tmp folder that the system uses for temporary storage of files. This folder in some cases might at least need 2x the size of the backup of available space.
+ HOME_FOLDER: Where the backups software installation files live
+ (Optional) LOCAL_BACKUP: if the server needs to keep local backups, this is the folder where they will be kept.
+ LOG_FOLDER: Folder or to store logs or specific file name where to store the logs.

### General tips to keep present:

+ Every section is flexible to add as many parameters as the specific module to be execute needs.
+ The only section with a compulsory name is GENERAL, because it has parameters that are used by all the other modules. The rest of the executable modules can be called any name, as long a you use a few key words (from 0 to 3 depending on how special the module is; development language, path, executable name) that explain how to find and execute.
+ The config file is the same for windows and Linux, what changes is the OS specific parameters.
+ The size should be a number integer that represents the MB size of one split part.
+ The file paths supplied to the different sections can be in any of the POSIX formats as absolute paths, relative paths, etc. The path ending in / or not should not cause problems to the diferent scripts and if it does a bug case should be opened.
+ We are working now on making the system also able to work with windows paths, but this is still a work in progress
+ The comma (,) at the end of a line means there is a sibling instruction after the one your are working on. This is JSON standard.
+ Keep present that all the parameters from configuration section of the plugins are passed to the class as a python dictionary when  pass parameter to the class when costructed. So it's your duty to parse this dictionary if you need config parameters.
+ The credentials, configs and keyfiles is advisable to be added to /etc instead of the current paths, this are just testing and development paths that are used currently for development. The script should be flexible engouh to have the configs anywhere. The specific standard is to be still agreed on.



### Section example
The following is a real working section that calls and executes external colde to compress a fileset.

      "FILESET":{
        "ACTION": "execute",
        "NAME": "filesbackup",
        "EXECUTE_WITH": "python",
        "EXECUTABLE": "",
        "PARAMETERS": {
          "FILESET_INCLUDE": "/etc /Users/cncuser/Documents/",
          "FILESET_EXCLUDE": "/Users/cncuser/Documents/Trabajo /Users/cncuser/Documents/Install/ /Users/cncuser/Documents/Personal"
        }
      }

**Line by line explanation**
 "FILESET":{ Defines a section beginning, the name can be anything, but as a convention is good to give it a name according to it's content.
 "ACTION": "execute", The kay word ACTION says to the script the now I want to say what to do in the section, there are 2 possible options defined for now:
 + execute: means an external code script is going to be executed.
 + load: a dynamic module will be loaded. There is a slide but important difference between "execute" and "load", load is to execute native python code in the for of dynamic imports while the other executes external independent scripts that can be done using any programming language as long as it follows some basic rules.
 + "NAME": "filesbackup", NAME is to specify the name of the folder where to find the plugin or script to load/execute. Is advised to call the modules the same name of the folder, but is not a requirement. Then "filesbackup" is the name of the external script to be executed in this case.
 + (Optional) "EXECUTE_WITH": "python", Is to know what type of code you need to execute, if your code is python, then you do not need to specify.
 + (Optional) "EXECUTABLE": "", is to know which one is the executable file in the module.
 + (Optional) "PARAMETERS": { This subsection is to pass parameters to the module to be executed/loaded. Inside you add parameters that you want the plugin/script to receive.
 + (Optional, specific to the plugin or script to load or execute) "FILESET_INCLUDE": "/etc /Users/cncuser/Documents/", The parameters are all depending on what you need to execute your code. Every section can have different parameters depending on the way it was programmed.

**The plugins also need a config section similar to this:**

      "SIZE":{
        "ACTION": "load",
        "FROM": "tools",
        "FILENAME": "size_calculation",
        "CLASS": "SizeCalculation",
        "PARAMETERS": {
          "OBJECTIVES": "/Users/cncuser/Downloads/backup/encrypted"
        }
      }
This is a working plugin that only calculates the size of the files to be backed up.
### Other Current working sections and specific explanations

**MySQL Dump:**


      "DBSBACKUP": {
        "ACTION": "execute",
        "NAME": "mysql_backup",
        "EXECUTABLE": "mysql_dump.py",
        "EXECUTE_WITH": "python",
        "PARAMETERS": {
          "CREDENTIAL_PATH": "/Users/cncuser/Documents/py/nc-backup-py/conf/mysql.credentials",
          "CONF_PATH": "/etc/my.cnf",
          "DATA_DIR": "/usr/local/var/mysql",
          "MY_INSTANCES": "3306",
          "LOG": "/usr/local/var/mysql/Abel-Guzman-Sanchezs-MacBook-Air.local.err",
          "BINLOG_PATH": "/usr/local/var/mysql/",
          "BINLOG_FILE_PREFIX": "mysql-bin",
          "DESTINATION": "/Users/cncuser/Downloads/backup",
          "TAR_COMMAND": "sudo /usr/local/Cellar/gnu-tar/1.28/bin/tar czf ",
          "MYSQL_DUMP_BINARY": "/usr/bin/mysql",
          "MYSQL_BINARY": "/usr/bin/mysql",
          "PREFIX_FOLDER": "mydump"
        }
      }

This section executes a external script that executes a dump on the MySQL DB. Some parameters implementations are still pending or not completed.

**Compression:**

      "COMPRESSION": {
        "ACTION": "execute",
        "NAME": "compression",
        "EXECUTABLE": "",
        "EXECUTE_WITH": "",
        "PARAMETERS": {
          "OBJECTIVES": "/Users/cncuser/Downloads/backup/files /Users/cncuser/Downloads/backup/mydump",
          "DESTINATION": "/Users/cncuser/Downloads/backup/compressed",
          "REMOVE_OBJECTIVES": "True"
        }
      }

This section takes a set of folders and compresses them. The parameters "REMOVE_OBJECTIVES": "True" means that the script will remove the fileset passed as parameters.
We are discussing the possibility of changing "OBJECTIVES" in all sections to some other candidate word like FILESETS. If this change is finally implemented the development changes are not a lot.

**Encryption**

      "ENCRYPTION": {
        "ACTION": "execute",
        "NAME": "encryption",
        "PARAMETERS": {
          "KEY_FILE": "/Users/cncuser/Documents/py/nc-backup-py/conf/key_file",
          "FILE_SIZE": "1",
          "OBJECTIVES": "/Users/cncuser/Downloads/backup/compressed",
          "DESTINATION":"/Users/cncuser/Downloads/backup/encrypted",
          "REMOVE_OBJECTIVES": "True"
        }
      }

This section as the name indicates encrypts files, but also splits long files according to FILE_SIZE give in MB. "KEY_FILE" is the path to the key file, the

**Storage**

      "STORAGE": {
        "ACTION": "execute",
        "NAME": "storage",
        "PARAMETERS":{
          "OBJECTIVES": "/Users/cncuser/Downloads/backup/encrypted",
          "DESTINATION":"s3",
          "BUCKET_NAME": "cncbackup",
          "UPLOAD_COMMAND": "aws s3 cp",
          "REMOVE_OBJECTIVES": "True"
        }
      }

This section is to store the backup, in this case s3. S3 is the only current backend implemented, but the script is supposed to support various backends including OSS, SSH, etc.

AWS CLI integration
Q: Does the AWS CLI validate checksums?¶
The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios.
Upload
The AWS CLI will calculate and auto-populate the Content-MD5 header for both standard and multipart uploads. If the checksum that S3 calculates does not match the Content-MD5 provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See aws help returncodes for more information.

# How to decrypt

# LICENSE

To be defined


# Others
UCLoud using sdk:
+ The script is able to do UCLOUD images of systems.
+ Nett to develop to make HDD snapshots.
Added here:
+ host_image_run.py
+ hdd_snapshot_run.py
#使用方法
打开 cp config.simple.py config.py 修改以下配置
#配置公私钥 公私钥请到用户中心获取
#   public_key  = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#   private_key = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
#   project_id = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx" #项目ID 请从dashbord 获取
#
#
#配置api地址'''
#   有外网IP主机使用
#   base_url    = "https://api.ucloud.cn"
#
send_sms.py 使用示范
python send_sms.py "13777777777|137xxxxxxxx|138xxxxxxxx" "测试短信"
#监控脚本示范建议加入crontab 1分钟一次

# Authors:
Abel Guzman

# Report bugs at:
+ abel.guzman (at) chinanetcloud.com
