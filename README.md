-Project name: nc-backup-py.

-Executable Script:

+ backup.py: Main script that can execute and control other scripts execution (needs arguments)
+ compression.py: compression script (needs arguments)
+ encryption.py Encryption and decryption script. (needs arguments)
+ filesbackup.py does backups of filesets with exclusions (needs arguments)
+ storage.py connects and saves files to different storages (done local and AWS S3). (needs arguments)
+ MySQl backup.

-Pending Scripts:
+ mongo
+ reporting
+ OSS storage
+ snapshots for different storages.
+ clean up scripts for local and remote files.
+ Windows compatibility:
+ Active directory backup
+ ms-sql backup.

-We also have available a module feature in the configs available through configuration as well. current modules:
+ tools/size_calculation.py: Size calculation


-Tools: every module or script include or make use of a set of tools included in tools folder.
+ date_str_utils.py
+ filesystem_handling
+ os_works
+ requests_utils
+ size calculation (This is also a module)

Requirements:
-
python 2.7

Python modules

-requests

-Crypto (Actually Crypto.Cipher)

python 2.6 also requires:
-argparse

ROAD MAP:
-Storage (local DONE)

-Communications (reports basic DONE)

-clean ups

-DBS

-logs

Bug:

Issues:
- TC_TIME env variable and other languague related variable that might stop execution with CHinese and types of characters.
- Current code should have create_preconfitions and delete_files moved to the new class filesystem_handling in tools

Next Release:
-Scheduler
-Improve Flow control
-Other?
-Add hostname to logs.


Done to be tested:
-Master
-Filesbackup
-Compression
-Pending Encryption

The JSON config file.

Introduction
We have a .json config file as the sole config for all modules and scripts used. Please find 2 sample file attached, one for Linux and one for windows.
Maybe at some point in the future I would implement being able to have more than one .json config file that can be included from a central file. Something like and include feature.

Then about include and exclude, every module receives a group of parameters. From a special optional section that looks like this in the case of exclude and include.

    "FILESET":{
    (...)
    "PARAMETERS": {
      "FILESET_INCLUDE": "c:\\backup\\backup_test_a C:\\Zabbix\\Log C:\\backup_test_b\\backup_test_1",
      "FILESET_EXCLUDE": "C:\\backup_test_b\\backup_test_1\\test_2.txt"
    }
    (...)
    }

Notice: FILESET, in this case is the name of a custom module.
Aside from that the config file has a compulsory section called GENERAL, where the user is supposed to specify general parameters that are used by most modules and passed to all of them. It looks like this:


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

Every section is flexible to add as many parameters as the specific module to be execute needs.

The only module with a compulsory name is GENERAL, because it has parameters that are used by all the other modules. The rest of the executable modules can be called any name, as long a you use a few key words (from 0 to 3 depending on how special the module is; development language, path, executable name) that explain how to find and execute.

The config file is the same for windows and Linux, what changes is the OS specific parameters.

The size should be a number integer that represents the MB size of one split part.

Execution of the main script:
e.g.:
python backup.py -r -c conf/conf.json


Plugins:
-Should have 3 callable functions:
+ config_plugin: Need to implement a way to pass arguments with something like *args
+ works_execution: can only print stuff.

You need to use the login features to work with it.
+ output: output final result.

Keep present that all the parameters from configuration section of the
plugins are passed to the class as a python dictionary when  pass parameter to
the class when costructed. So ot's your duty to parse this dictionary if you
need config parameters.

The plugins also need a config section similar to this:

      "SIZE":{
        "ACTION": "load",
        "FROM": "tools",
        "FILENAME": "size_calculation",
        "CLASS": "SizeCalculation",
        "PARAMETERS": {
          "OBJECTIVES": "/Users/cncuser/Downloads/backup/encrypted"
        }
      }


AWS CLI integration
Q: Does the AWS CLI validate checksums?¶
The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios.

Upload

The AWS CLI will calculate and auto-populate the Content-MD5 header for both standard and multipart uploads. If the checksum that S3 calculates does not match the Content-MD5 provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See aws help returncodes for more information.
LICENSE

Authors:
Abel Guzman

Report bugs at:
abel.guzman@chinanetcloud.com


ucloud sdk:
Abel Guzman added here:
host_image_run.py
hdd_snapshot_run.py

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