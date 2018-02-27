## Configuration -  The JSON config file

## Introduction
The conf.json file is the sole configuration file for all modules and scripts used. This is standard JSON with a few Keywords specific to the software and sections.

Location: /etc/nc-backup-py/conf.json
Examples: /etc/nc-backup-py/Examples

The file is list of modules to be executed. The first and only mandatory section is general. For more information see [General Section docs](GENERAL.md)

Each module in this json array is executed sequentially, one after the other.

A typical configuration flow looks like this.

* GENERAL (Initialize)

* FILESET (Copy and archive files)

* MYSQL / MONGO / POSTGRES (Optional, to add database dumps)

* COMPRESSION (Compress files)

* ENCRYPTION (Encrypt files)

* SIZE (Calculate size of backup)

* STORAGE_S3 (Send to AWS S3)

* STORAGE_LOCAL (Move files to local backup)

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

## The modules (plugins)


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

### Sections and Modules

# The GENERAL section

see [General](GENERAL.md)

# Files Backup

This section is used to add files to the backup.

see [File Backup](FILESBACKUP.md)

#### MySQL Dump

This section executes a external script that executes a dump on a MySQL DB. Some parameters implementations are still pending or not completed.

see [MySQL](MYSQL.md)

#### Mongo DB

This section executes a external script that executes a dump on a MongoDB DB. This is still in testing Many parameters implementations are still pending or not completed.

see [MongoDB](MONGO.md)

#### Postgresql

This section executes a external script that executes a dump on a PostgreSQL DB. This is still in testing Many parameters implementations are still pending or not completed.

see [PostgreSQL](MONGO.md)

#### Compression

This section compresses the files and database dumps (if any) added above.

see [Compression](COMPRESSION.md)

#### Encryption

This section encrypts the compressed files.

see [Encryption](ENCRYPTION.md)

#### Storage Configuration

For instructions on how to configure storage and install related 3rd party tools.

see [STORAGE](STORAGE.md)


#### QA
```json
      "QA":{
        "ACTION": "load",
        "FROM": "qa",
        "FILENAME": "qa",
        "CLASS": "QA"
     }
```
This feature is still under development in test conceptual phase, the idea is for the script to be able to detect the problems on it's own and at some point even auto-fix them. For now it's just included as a proof of concept module it only checks that the user running the script is ncbackup and logs a warning if the user is wrong. Please provide feedback on the things that the script is supposed to QA for so the development can be carried out following the best and more useful practices.


## General tips to keep present:

* Every section is flexible to add as many parameters as the specific module to be execute needs.
* The only section with a compulsory name is GENERAL, because it has parameters that are used by all the other modules. The rest of the executable modules can be called any name, as long a you use a few key words (from 0 to 3 depending on how special the module is; development language, path, executable name) that explain how to find and execute.
* The config file is the same for windows and Linux, what changes is the OS specific parameters.
* The size should be a number integer that represents the MB size of one split part.
* The file paths supplied to the different sections can be in any of the POSIX formats as absolute paths, relative paths, etc. The path ending in / or not should not cause problems to the diferent scripts and if it does a bug case should be opened.
* We are working now on making the system also able to work with windows paths, but this is still a work in progress
* The comma (,) at the end of a line means there is a sibling instruction after the one your are working on. This is JSON standard.
* Keep present that all the parameters from configuration section of the plugins are passed to the class as a python dictionary when pass parameter to the class when costructed. So it's your duty to parse this dictionary if you need config parameters.
* The credentials, configs and keyfiles is advisable to be added to /etc instead of the current paths, this are just testing and development paths that are used currently for development. The script should be flexible engouh to have the configs anywhere. The specific standard is to be still agreed on.


### General json keys

* `ACTION` - tells the software what to do with the section of the configuration. for now it has 2 options that actually do something. In other words how to loadthe code. Execute and load, find theit entries for explanations of what they do.
* `execute` - Key word for the ACTION parameter, execute means that this section executes and external script that is not dependant on the main script and needs it's own way to be executed.
* `load` - Key word for the ACTION parameter, load means that this section loads a pluging via importing it dynamically. the code doe not depend on each other but the dynamically loaded code has to follow certain structure.
* `NAME` Name of and external script to execute. the software is going to look for a folder called the name spacified in this parameter
* `FROM` - folder where the plugin is located. This parameter might be merged with NAME in future versions.
* `EXECUTABLE` - Optional parameter to say the name of the executable script inside the folder called NAME. This parameter needs to be specified only if the external script is not python or if the external script's name if different from the folder where it is. So the default value is the same as NAME parameter if not specified.
* `EXECUTE_WITH` - Optional parameter to say what software to use to execute. The software is able to execute any type of scripts; bash, php, perl, python, the default value is python if not specified.
