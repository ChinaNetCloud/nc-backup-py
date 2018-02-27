## Configuration

### The JSON config file

#### Introduction
A .json config file is the sole config for all modules and scripts used. This is standard JSON; with a few Keywords specific to the software and sections. Maybe at some point in the future we might need to implement being able to have more than one .json config file that can be included from a central file. Something like and include feature. The config only has one mandatory section It looks like this:
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
#### The GENERAL section

Basics of the .json file:
* `HOSTNAME`: is the China Net Cloud hostname e.g. srv-nc-zabbix-db1, it can actually be any name, but we should keep it like that to follow out standards.
* `WORK_FOLDER`: is a tmp folder that the system uses for temporary storage of files. This folder in some cases might at least need 2x the size of the backup of available space.
* `HOME_FOLDER`: Where the backups software installation files live
(Optional) `LOCAL_BACKUP`: if the server needs to keep local backups, this is the folder where they will be kept.
* `LOG_FOLDER`: Folder or to store logs or specific file name where to store the logs.
* `DISK_SPACE_CHECK`: is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
* `DISK_SPACE_THRESHOLD`: Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%.

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
```json
  "FILESET": {
    "ACTION": "execute",
    "NAME": "filesbackup",
    "PARAMETERS": {
      "__READTHIS": "Space delimited paths to backup (recursive)",
      "FILESET_INCLUDE": "/etc /home/user",
      "__READTHIS": "Space delimited paths to exclude (within FILESET_INCLUDE)",
      "FILESET_EXCLUDE": ""
    }
  },
```
Notice: `FILESET_INCLUDE` can not be "/"

##### Optional parameters
This section as most of the others have most of it's parameters as optional. For a default Cent OS 6 or 7 configuration this section should work the same as the section before as it would assume default configurations according to our new standards.
```json
      "FILESET":{
        "ACTION": "execute",
        "NAME": "filesbackup"
     }
```

##### Line by line explanation
* `"FILESET":{` Defines a section beginning, the name can be anything, but as a convention is good to give it a name according to it's content.
* `"ACTION":` "execute", The kay word ACTION says to the script the now I want to say what to do in the section, there are 2 possible options defined for now:
* `execute:` means an external code script is going to be executed.
* `load:` a dynamic module will be loaded. There is a slide but important difference between "execute" and "load", load is to execute native python code in the for of dynamic imports while the other executes external independent scripts that can be done using any programming language as long as it follows some basic rules.
* `"NAME": "filesbackup"`, `NAME` is to specify the name of the folder where to find the plugin or script to load/execute. Is advised to call the modules the same name of the folder, but is not a requirement. Then "filesbackup" is the name of the external script to be executed in this case.
* (Optional) `"EXECUTE_WITH": "python",` Is to know what type of code you need to execute, if your code is python, then you do not need to specify.
* (Optional) `"EXECUTABLE": "",` is to know which one is the executable file in the module.
* (Optional) `"PARAMETERS": {` This subsection is to pass parameters to the module to be executed/loaded. Inside you add parameters that you want the plugin/script to receive.
* (Optional, specific to the plugin or script to load or execute) `"FILESET_INCLUDE": "/etc /Users/cncuser/Documents/",` The parameters are all depending on what you need to execute your code. Every section can have different parameters depending on the way it was programmed.

##### The plugins

Plugins also need a config section similar to this:
```json
  "SIZE":{
    "ACTION": "load",
    "FROM": "tools",
    "FILENAME": "size_calculation",
    "CLASS": "SizeCalculation",
    "PARAMETERS": {
        "TARGETS": "/Users/cncuser/Downloads/backup/encrypted"
    }
  }
```
This is a working plugin that only calculates the size of the files to be backed up.

#### Sections and modules available

#### MySQL Dump:

This section executes a external script that executes a dump on the MySQL DB. Some parameters implementations are still pending or not completed.

see [MySQL](docs/MYSQL.md)

#### Mongo DB

see [MongoDB](docs/MONGO.md)

#### Postgresql

see [PostgreSQL](docs/MONGO.md)


Notice: This is a plugin instead of an executable independent script.
Notice: The script can exclude databases with EXCLUDE_DB, but is can not exclude tables yet.

#### Compression

see [Compression](docs/COMPRESSION.md)

#### Encryption

see [Encryption](docs/ENCRYPTION.md)

#### Storage Configuration

[STORAGE](STORAGE.md) for instructions on how to configure storage and install related 3rd party tools.

##### QA
```json
      "QA":{
        "ACTION": "load",
        "FROM": "qa",
        "FILENAME": "qa",
        "CLASS": "QA"
     }
```
This feature is still under development in test conceptual phase, the idea is for the script to be able to detect the problems on it's own and at some point even auto-fix them. For now it's just included as a proof of concept module it only checks that the user running the script is ncbackup and logs a warning if the user is wrong. Please provide feedback on the things that the script is supposed to QA for so the development can be carried out following the best and more useful practices.

#### AWS CLI integration

Q: Does the AWS CLI validate checksums?
The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios. Upload The AWS CLI will calculate and auto-populate the Content-MD5 header for both standard and multipart uploads. If the checksum that S3 calculates does not match the Content-MD5 provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See aws help returncodes for more information. Taken from AWS CLI FAQ


### Reference Manual the JSON file:

## General section

* `GENERAL` - Identifies the main section of the configuration. The content of this section is passed to most scripts and plugins executed.
* `HOSTNAME` - Server unique identificator name.
* `WORK_FOLDER` - Temporary folder to do the works.
* `LOCAL_BACKUP` - Place to keep the copies of local backups if this option is selected. This will be probably deprecated in firther versions of the software.
* `HOME_FOLDER` - Place where the source code is located (Install folder).
* `LOG_FOLDER` - Path to log file, this variable will be modified in the next version of the software.
* `DISK_SPACE_CHECK` - is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
* `DISK_SPACE_THRESHOLD` - Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%. This value determines how to react to HDD getting full. if you set it to 20% then you will get a warning if the HDD space is less than 20%. If the space goes under half the threshold (20% in this case, so 10%) so instead of a warning you will get a Critical or Error instead. Now if the space left goes under 10 times lower than the threshold (in the case of 20% it will be 2%), then the backup system will stop execution immediately and send a failure report.

### Sections and key words

* `ACTION` - tells the software what to do with the section of the configuration. for now it has 2 options that actually do something. In other words how to loadthe code. Execute and load, find theit entries for explanations of what they do.
* `execute` - Key word for the ACTION parameter, execute means that this section executes and external script that is not dependant on the main script and needs it's own way to be executed.
* `load` - Key word for the ACTION parameter, load means that this section loads a pluging via importing it dynamically. the code doe not depend on each other but the dynamically loaded code has to follow certain structure.
* `NAME` Name of and external script to execute. the software is going to look for a folder called the name spacified in this parameter
* `FROM` - folder where the plugin is located. This parameter might be merged with NAME in future versions.
* `EXECUTABLE` - Optional parameter to say the name of the executable script inside the folder called NAME. This parameter needs to be specified only if the external script is not python or if the external script's name if different from the folder where it is. So the default value is the same as NAME parameter if not specified.
* `EXECUTE_WITH` - Optional parameter to say what software to use to execute. The software is able to execute any type of scripts; bash, php, perl, python, the default value is python if not specified.
* `PARAMETERS` - Optional paramter to specify parameters to pass to the script ot plugin.
* `TAR_COMMAND` - Optimal parameters, to execute tar command on custom systems. the default calue is normally 'sudo /bin/tar czCf /' if not specified. this parameter can be specified in the following sections: FILESET, DBSBACKUP, COMPRESSION
* `TARGETS` or `OBJECTIVES`- This parameter is to specify a group of targets to work with, is used by most scripts and plugins. We are in a discussion to probably will completely remove OBJECTIVES in the near futire, please do not use it for configurations anymore.
* `DESTINATION` - Where to store the results. Used by most modules.
* `REMOVE_TARGETS` / `REMOVE_OBJECTIVES` - If you want to remove the Target (OBJECTIVES) files or not. it accepts two possible values; True or False. The default value is True. REMOVE_OBJECTIVES will be deprecated in later versions in favor of REMOVE_TARGETS.
* `True` - Yes
* `False` - Not, No
* `KEY_FILE` - parameter used by the encryption and decryption script as key. this parameter should contain the path to a key file, normally in /etc.
* `FILE_SIZE` - Size of the encrypted files, always given in MB. The next versions might include other units if deamed required.
