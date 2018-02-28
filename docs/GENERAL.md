# The GENERAL section

The only section with a compulsory name is GENERAL, because it has parameters that are used by all the other modules. The rest of the executable modules can be called any name, as long a you use a few key words (from 0 to 3 depending on how special the module is; development language, path, executable name) that explain how to find and execute.

```json
  "GENERAL": {
    "HOSTNAME": "srv-nc-template-host-config",
    "WORK_FOLDER": "/opt/backup",
    "HOME_FOLDER": "/var/lib/nc-backup-py/",
    "LOG_FOLDER": "/var/log/nc-backup-py/nc-backup-py.log",
    "__READTHIS": "If you don't want backup reports sent remove the three lines below this.",
    "MESSAGE_CONFIG_COMMAND": "https://backupreporter.<Change this to your domain>.com/backup_service.php",
    "MESSAGE_CONFIG_METHOD": "post",
    "__Methods": "post|e-mail|sms|wechat,etc"
  },
```

## Parameters

* `GENERAL` - Identifies the main section of the configuration. The content of this section is passed to most scripts and plugins executed.
* `HOSTNAME` - Server unique identificator name.
* `WORK_FOLDER` - Temporary folder to do the works.
* `LOCAL_BACKUP` - Place to keep the copies of local backups if this option is selected. This will be probably deprecated in firther versions of the software.
* `HOME_FOLDER` - Place where the source code is located (Install folder).
* `LOG_FOLDER` - Path to log file, this variable will be modified in the next version of the software.
* `DISK_SPACE_CHECK` - is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
* `DISK_SPACE_THRESHOLD` - Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%. This value determines how to react to HDD getting full. if you set it to 20% then you will get a warning if the HDD space is less than 20%. If the space goes under half the threshold (20% in this case, so 10%) so instead of a warning you will get a Critical or Error instead. Now if the space left goes under 10 times lower than the threshold (in the case of 20% it will be 2%), then the backup system will stop execution immediately and send a failure report.
