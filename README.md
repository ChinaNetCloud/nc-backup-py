# nc-backup-py

## Introduction

nc-backup-py intends to be a comprehensive one stop solution for backups. It can backup files, mySQL databases, Postgres databases, LVM, MongoDB and many more to another drive, to the cloud or to another server via the network.

To quickly set up a backup and never lose your files again go to [Quick Start](#quick-start)

See [Features](#features) for a complete list of current and planned Features.
See [How to contribute](#how-to-contribute) if you would like to join us.

If you are interested on leaning about the structure of the project
See [OVERVIEW](docs/OVERVIEW.md)

If you think the project is useful or has potential, please add a star.

## Requirements

The script is tested for the following requirements. It maybe possible to run on other configurations. If you can run it on other configurations successfully please let us know by creating an issue.

* Operating System
  * Linux
    - Centos > 6
    - Ubuntu > 14.04

* Python >= 2.6 (Python 3 not supported)
* `pip` (Python)
* `gcc`, `python-devel` (To build dependencies)  
* `python-crypto` (Optional, install if pip fails to install Crypto)

  * RHEL7, CentOS7, Fedora7
  ```bash
  $ sudo yum install https://mirrors.aliyun.com/epel/epel-release-latest-7.noarch.rpm # If you don't have EPEL/pip installed
  $ sudo yum install python-crypto gcc python-devel python-pip # RHEL7, Fedora7, centOS7
  $ sudo yum groupinstall 'Development Tools' -y # If development tools are not available.
  ```
  * RHEL6, CentOS6, Fedora6
  ```bash
  $ sudo yum install https://mirrors.aliyun.com/epel/epel-release-latest-6.noarch.rpm # If you don't have EPEL/pip installed
  $ sudo yum install python-crypto gcc python-devel python-pip # RHEL6, Fedora6, centOS6
  $ sudo yum groupinstall 'Development Tools' -y # If development tools are not available.
  ```
  * Debian, Ubuntu
  ```bash
  $ sudo apt-get install python-crypto python-dev python-pip # Debian, Ubuntu
  ```


## Quick Start

This quick start is to download, install and configure the `master` branch to upload files to AWS S3.

See [INSTALLATION](docs/INSTALLATION.md) for more information on customizing your install.
See [CONFIGURATION](docs/CONFIGURATION_FILE.md) to view and configure all available features.

* Clone or Download the git repository and change directory .
  ```bash
  $ git clone --depth=1 --branch master https://github.com/ChinaNetCloud/nc-backup-py.git
  $ cd nc-backup-py
  ```

  *or*

  ```bash
  $ wget -O nc-backup-py.zip https://github.com/ChinaNetCloud/nc-backup-py/archive/master.zip
  $ unzip nc-backup-py.zip
  $ cd nc-backup-py-master
  ```

* *Optionally* clone the branch you want. *Do this only if you know what this is for.*
  ```bash
  $ git clone --depth=1 --branch test-dev https://github.com/ChinaNetCloud/nc-backup-py.git
  ```

* Run setup
  ```bash
  $ cd nc-backup-py
  $ sudo pip install --upgrade .
  ```

  *or*, after installing the required dependencies using pip

  ```bash
  $ sudo python setup.py
  ```

* Edit configuration

  This quick start works for uploading your local files to AWS S3. See [CONFIGURATION](docs/CONFIGURATION.md) for a complete guide and documentation.

  nc-backup-py reads configuration from a json file and executes it sequentially. Each first level section (item) in the json list is an individual module that gets executed.

  The "GENERAL" section is the only mandatory section. **Use only the modules you need.**

  The other sections do one particular job, for example "COMPRESSION" compresses files and the "STORAGE_S3" uploads files.

  It is also possible to run any command using the "CUSTOM_COMMAND" section. See [CUSTOM_COMMAND](docs/CUSTOM_COMMAND.md)

  You can also define a customized storage location. See [STORAGE](docs/STORAGE.md#customized-storage)

  1. Change the AWS S3 bucket name under the `STORAGE_S3` section.
    ```json
    "ARGS_DICT": "{'BUCKET': 'yourbucket'}",
    ```

  2. Optionally send backup reports via HTTP POST. Or you can remove it.
    ```json
    "MESSAGE_CONFIG_COMMAND": "https://backupreporter.service.<yourdomain>.com/backup_report_service/backup_service.php",
    "MESSAGE_CONFIG_METHOD": "post",
    ```

  3. Include the files you want, it will be backed up recursively. You can exclude files within this directory by using `FILESET_EXCLUDE`
    ```json
    "FILESET": {
      "ACTION": "execute",
      "NAME": "filesbackup",
      "PARAMETERS": {
        "FILESET_INCLUDE": "/etc",
        "FILESET_EXCLUDE": ""
      }
    }
    ```

  4. Configure storage for AWS CLI or AWS roles.

    For more storage options see [STORAGE](docs/STORAGE.md#customized-storage)

    * AWS CLI

      - Install - See [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

      - Configure - See [Quick Configuration](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)

      - Please switch user to `ncbackup` before configuring AWS CLI
        ```bash
        # su - ncbackup -s /bin/bash
        $ whoami && pwd
        ncbackup
        /home/ncbackup
        $ aws configure
        AWS Access Key ID [None]: <ACCESS KEY ID>
        AWS Secret Access Key [None]: <ACCESS KEY>
        Default region name [None]: <REGION>
        Default output format [None]: json
        ```

    * AWS roles
      - See [IAM Roles for Amazon EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)


  * Execute Backup manually
    ```bash
    $ sudo -u ncbackup python /var/lib/nc-backup-py/backup.py -r -c /etc/nc-backup-py/conf.json -l WARNING
    ```

  * ***IMPORTANT*** Copy and save your key file. If you lose this, you will not be able to decrypt your files.

    The first time you run your backup script with **ENCRYPTION** enabled, it will create a key at `/etc/nc-backup-py/key_file`. Please copy this and store it in a secure location. (ex: keepass) You will require this to decrypt the files later.

    ```bash
    $ ls /etc/nc-backup-py/key_file
    $ cat /etc/nc-backup-py/key_file
    ```

  * Optionally add a cronjob
    ```bash
    $ crontab -eu ncbackup
    00 03 * * * python /var/lib/nc-backup-py/backup.py -r -c /etc/nc-backup-py/conf.json
    ```

  * Provide feedback on [Issue](https://github.com/ChinaNetCloud/nc-backup-py/issues) for support

## Decryption

Download the files to /opt/backup e.g.:
```bash
$ aws s3 cp s3://cnc-bj-backup/srv-nc-bj-zabbix-qa1/20160705_042923.tar.gz.crypt.000 /opt/backup
# Execute the decryption command:
# For a encrypted archive "20160705_042923.tar.gz.crypt.000"
$ ls
$ 20160705_042923.tar.gz.crypt.000
$ python /var/lib/nc-backup-py/encryption/encryption.py -d \
--KEY_FILE "/etc/nc-backup-py/key_file" \
--OBJECTIVES "20171106_105027.tar.gz.crypt.000" \
--DESTINATION "20171106_105027.tar.gz" \
--HOME_FOLDER "/var/lib/nc-backup-py"
```

For more information see [decryption](docs/DECRYPTION.md)

## Uninstall

```bash
pip uninstall nc-backup-py
```
* To remove scripts
```bash
sudo rm -rf /var/lib/nc-backup-py/
```
* To remove ncbackup user
```bash
sudo userdel ncbackup && /etc/sudoers.d/ncbackup
```
* To remove sudo access.
```bash
rm -rf /etc/sudoers.d/ncbackup
```
* To remove logs
```bash
sudo rm -rf /var/log/nc-backup-py
```
* To remove configuration
```bash
sudo rm -rf /etc/nc-backup-py
```
* To remove all
```bash
pip uninstall nc-backup-py
sudo rm -rf /var/lib/nc-backup-py/ /etc/nc-backup-py/ /var/log/nc-backup-py/
sudo userdel ncbackup && rm -rf /etc/sudoers.d/ncbackup
```

## Features

#### Features Available
* Backup to multiple clouds storages: AWS S3, Aliyun (Alibaba), Mounted writable drive.
* Compression, Encryption, Decryption, Split files
* Backup of regular files and Multiple Databases: MySQL Dump, Mongo DB dump, Postgres SQL dump.
* Send POST message reports to custom URL. Report includes Success, size, server, log, etc.
* Retry failed uploads and report messages.
* Extendable with plugins and scripts:
  * Run custom separate program on any programming language,
  * Accept integrated plugins; this are Python special classes that can be understood by nc-backup-py.

#### Features Planned
* MySQL Xtrabackup
* Avoid multiple compression operations. This can actually be considered a bug.
* Optionally use or Not local drive to consolidate backup files (Direct Streaming to remote destination).
* SSH storage backup
* Send report messages using e-mail, sms, wechat
* Improve documentation.

#### Features under development
* Windows support.
* ionice and network nice management.
* snapshots for different storages.
* clean up scripts for local and remote files.
* Windows Server compatibility
* Windows Server compatibility
* Active directory backup
* ms-sql backup.


## How to contribute

We appreciate all contributions and look forward to your help.

#### Developer:
1. Install the `test-dev` branch and get it to work.

2. Create an [Issue](https://github.com/ChinaNetCloud/nc-backup-py/issues) and start discussion providing as many details as possible, with maintainers team.

3. Once the issue is accepted you will be added to the team as contributor, then you can start development.

4. Commit to your own branch.

5. Send merge request to test test-dev once done with your feature and update on Issues.

6. Iterate :P.

***ChinaNetCloud/nc-backup-py is licensed under the
[Apache License 2.0](LICENSE)***
