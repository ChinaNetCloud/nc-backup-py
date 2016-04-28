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