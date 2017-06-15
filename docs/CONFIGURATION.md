## Configuration

### The JSON config file

#### Introduction
A .json config file is the sole config for all modules and scripts used. This is standard JSON; with a few Keywords specific to the software and sections. Maybe at some point in the future we might need to implement being able to have more than one .json config file that can be included from a central file. Something like and include feature. The config only has one mandatory section It looks like this:

    `{
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
    }`
    
#### The GENERAL section

Basics of the .json file:
`HOSTNAME`: is the China Net Cloud hostname e.g. srv-nc-zabbix-db1, it can actually be any name, but we should keep it like that to follow out standards.
`WORK_FOLDER`: is a tmp folder that the system uses for temporary storage of files. This folder in some cases might at least need 2x the size of the backup of available space.
`HOME_FOLDER`: Where the backups software installation files live
(Optional) `LOCAL_BACKUP`: if the server needs to keep local backups, this is the folder where they will be kept.
`LOG_FOLDER`: Folder or to store logs or specific file name where to store the logs.
`DISK_SPACE_CHECK`: is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
`DISK_SPACE_THRESHOLD`: Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%.

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

     `"FILESET":{
        "ACTION": "execute",
        "NAME": "filesbackup",
        "EXECUTE_WITH": "python",
        "EXECUTABLE": "",
        "PARAMETERS": {
            "FILESET_INCLUDE": "/etc /opt/ncscripts /var/spool/cron",
            "FILESET_EXCLUDE": ""
        }
     }`
Notice: `FILESET_INCLUDE` can not be "/"

##### Optional parameters
This section as most of the others have most of it's parameters as optional. For a default Cent OS 6 or 7 configuration this section should work the same as the section before as it would assume default configurations according to our new standards.

     `"FILESET":{
        "ACTION": "execute",
        "NAME": "filesbackup"
     }`
     
##### Line by line explanation
`"FILESET":{` Defines a section beginning, the name can be anything, but as a convention is good to give it a name according to it's content.
`"ACTION":` "execute", The kay word ACTION says to the script the now I want to say what to do in the section, there are 2 possible options defined for now:
`execute:` means an external code script is going to be executed.
`load:` a dynamic module will be loaded. There is a slide but important difference between "execute" and "load", load is to execute native python code in the for of dynamic imports while the other executes external independent scripts that can be done using any programming language as long as it follows some basic rules.
`"NAME": "filesbackup"`, `NAME` is to specify the name of the folder where to find the plugin or script to load/execute. Is advised to call the modules the same name of the folder, but is not a requirement. Then "filesbackup" is the name of the external script to be executed in this case.
(Optional) `"EXECUTE_WITH": "python",` Is to know what type of code you need to execute, if your code is python, then you do not need to specify.
(Optional) `"EXECUTABLE": "",` is to know which one is the executable file in the module.
(Optional) `"PARAMETERS": {` This subsection is to pass parameters to the module to be executed/loaded. Inside you add parameters that you want the plugin/script to receive.
(Optional, specific to the plugin or script to load or execute) `"FILESET_INCLUDE": "/etc /Users/cncuser/Documents/",` The parameters are all depending on what you need to execute your code. Every section can have different parameters depending on the way it was programmed.

##### The plugins

Plugins also need a config section similar to this:

     `"SIZE":{
        "ACTION": "load",
        "FROM": "tools",
        "FILENAME": "size_calculation",
        "CLASS": "SizeCalculation",
        "PARAMETERS": {
            "TARGETS": "/Users/cncuser/Downloads/backup/encrypted"
        }
     }`
     
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

    `"MONGODB":{
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
    }`
  
Notice: This is a plugin instead of an executable independent script.

#### Postgresql

Create backup user ncbackup in postgresql

`postgres=> create user ncbackup with password 'PASSWORD';`

Details about how to create user in pgsql, please refer to Basic postgresql management procedure

`Grant select privilege on all user_created tables to ncbackup
Customerdb=> grant select on $TABLE_NAME to ncbackup;`

You have to grant privilege one by one, of cource, you could also create a batch scipt to do it.

Create `.pgpass` file in `/home/ncbackup` with following contents, that is for backup script authenticaiton.
`localhost:*:*:ncbackup:$PASSWORD`
You should change the `$PASSWORD` part accordingly

Setup ownership and privilge like the following:

`[root@srv-xxx-xxx ~]# ls -l /home/ncbackup/.pgpass 
-rw------- 1 ncbackup ncbackup 34 Jun 12 17:04 /home/ncbackup/.pgpass
[root@srv-xxx-xxx ~]#`

Be careful, `600` permisions is a must when the backup will be restored, before you do anything, you must create all the user and database related to the backup, or the restore will fail

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

`-d`: is to say we are decrypting.
`--KEY_FILE "conf/key_file"`: is to indicate the path to the keyfile to used for decryption.
`--OBJECTIVES "/path/to/file(s)"`: It's to say where are the encrypted files to be decrypted. if the download is more than one file they need to have names that start with the same partern; the software asumes you mean wild card (*) at the end. In other words, the names should be like something like this filename.tar.gz.crypt.000, filename.tar.gz.crypt.001, filename.tar.gz.crypt.00N, so in this case yout path should contanin the common part's of the name "filename.tar.gz.crypt.00".
`--DESTINATION "path/and/name/of/tar.gz/file"`: this is the name and path that you want the resulting file to have after decryption
`--HOME_FOLDER "/path/to/source/code/nc-backup-py"`: this is for the encryption script to know where the whole backups software is installed.

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

`GENERAL` - Identifies the main section of the configuration. The content of this section is passed to most scripts and plugins executed.
`HOSTNAME` - Server unique identificator name.
`WORK_FOLDER` - Temporary folder to do the works.
`LOCAL_BACKUP` - Place to keep the copies of local backups if this option is selected. This will be probably deprecated in firther versions of the software.
`HOME_FOLDER` - Place where the source code is located (Install folder).
`LOG_FOLDER` - Path to log file, this variable will be modified in the next version of the software.
`DISK_SPACE_CHECK` - is and optional option to define if you want the system to check available space used on the partition where the work folder is mounted.
`DISK_SPACE_THRESHOLD` - Is the average disk given in (%) that you want the backups system to trigger alerts. This is an optional statement and the default value is 20%. This value determines how to react to HDD getting full. if you set it to 20% then you will get a warning if the HDD space is less than 20%. If the space goes under half the threshold (20% in this case, so 10%) so instead of a warning you will get a Critical or Error instead. Now if the space left goes under 10 times lower than the threshold (in the case of 20% it will be 2%), then the backup system will stop execution immediately and send a failure report.

### Sections and key words

`ACTION` - tells the software what to do with the section of the configuration. for now it has 2 options that actually do something. In other words how to loadthe code. Execute and load, find theit entries for explanations of what they do.
`execute` - Key word for the ACTION parameter, execute means that this section executes and external script that is not dependant on the main script and needs it's own way to be executed.
`load` - Key word for the ACTION parameter, load means that this section loads a pluging via importing it dynamically. the code doe not depend on each other but the dynamically loaded code has to follow certain structure.
`NAME` Name of and external script to execute. the software is going to look for a folder called the name spacified in this parameter
`FROM` - folder where the plugin is located. This parameter might be merged with NAME in future versions.
`EXECUTABLE` - Optional parameter to say the name of the executable script inside the folder called NAME. This parameter needs to be specified only if the external script is not python or if the external script's name if different from the folder where it is. So the default value is the same as NAME parameter if not specified.
`EXECUTE_WITH` - Optional parameter to say what software to use to execute. The software is able to execute any type of scripts; bash, php, perl, python, the default value is python if not specified.
`PARAMETERS` - Optional paramter to specify parameters to pass to the script ot plugin.
`TAR_COMMAND` - Optimal parameters, to execute tar command on custom systems. the default calue is normally 'sudo /bin/tar czCf /' if not specified. this parameter can be specified in the following sections: FILESET, DBSBACKUP, COMPRESSION
`TARGETS` or `OBJECTIVES`- This parameter is to specify a group of targets to work with, is used by most scripts and plugins. We are in a discussion to probably will completely remove OBJECTIVES in the near futire, please do not use it for configurations anymore.
`DESTINATION` - Where to store the results. Used by most modules.
`REMOVE_TARGETS` / `REMOVE_OBJECTIVES` - If you want to remove the Target (OBJECTIVES) files or not. it accepts two possible values; True or False. The default value is True. REMOVE_OBJECTIVES will be deprecated in later versions in favor of REMOVE_TARGETS.
`True` - Yes
`False` - Not, No
`KEY_FILE` - parameter used by the encryption and decryption script as key. this parameter should contain the path to a key file, normally in /etc.
`FILE_SIZE` - Size of the encrypted files, always given in MB. The next versions might include other units if deamed required.

## MYSQL Specifics:

`CREDENTIAL_PATH` - This is to specify the path to the MySQL credentials file. We will consider using the same Variable Name for other database systems.
`CONF_PATH` - This if for the path to MySQL my.cnf file (config file normally here /etc/my.cnf).
`DATA_DIR` - MySQL data dir, the company normally uses /var/lib/mysql/data
`MY_INSTANCES` - List space separated ports for the different instances running on a server default: "3306",
`BINLOG_PATH` - Path to binary logs for MySQL.
`BINLOG_FILE_PREFIX` - this is the beginning of the name normally defined my.cnf
`MYSQL_DUMP_BINARY` - Path to mysqlgdump binary executable file.
`MYSQL_BINARY` - Path to MySQL binary executable file.
`PREFIX_FOLDER` - Name of the folder and file prefix for MySQL backups inside the WORK_FOLDER.
`EXCLUDE_DB` - Database name to exclude.
`EXCLUDE_TABLE` Database and table names to exclude separated by a "." follow standard SQL notation e.g.: "mysql.user mysql.func mysql.event"
`BINLOG_DAYS` - Number of days of bin-logs to take.

#### Other MySQL instructions to be documented

    `"MONGODB":{
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
    }`


### Known issues 

#### ssl issues on python 2.6

You get the following warning:

`/usr/lib/python2.6/site-packages/pip/_vendor/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
 InsecurePlatformWarning`
 
Please ignore this message; the software works just fine, this is a problem with a deprecated ssl python library.

#### gpg-agent --daemon on python 2.6

If you see this error below:

`can not connect to /home/user/.gnupg/S.gpg-agent: No such file or directory`

Then launch gpg agent daemon:

`$ gpg-agent --daemon
GPG_AGENT_INFO=/tmp/gpg-Y1AjlZ/S.gpg-agent:2523:1; export GPG_AGENT_INFO;
then you’ll just have to create a symbolic link:
$ cp -fs /tmp/gpg-Y1AjlZ/S.gpg-agent ~/.gnupg/`