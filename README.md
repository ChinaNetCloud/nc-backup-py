# nc-backup-py

## Introduction

nc-backup-py intends to be a comprehensive one stop solution for backups. It can backup files, mySQL databases, Postgres databases, LVM, MongoDB and many more to another drive, to the cloud or to another server via the network.

To quickly set up a backup and never lose your files again go to [Quick Start](## Quick Start)

See [Features](## Features) for a complete list of current and planned Features.
See [How to contribute](## How to contribute) if you would like to join us.

If you are interested on leaning about the structure of the project
See [OVERVIEW](docs/OVERVIEW.md)

If you think the project is useful or has potential, please add a star.

## Requirements
* Operating System
  * Linux
  * Windows (in development)

* Python >= 2.6 (Python 3 not supported)
* `pip` (Python)
* `git` (Optional)
* `curl` or `wget`

## Quick Start

This quick start is to download, install and configure the `master` branch to upload files to AWS S3.

See [INSTALLATION](docs/INSTALLATION) for more information on customizing your install.
See [CONFIGURATION](docs/CONFIGURATION) to view and configure all available features.

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

  This quick start works for uploading you local files to AWS S3. See [CONFIGURATION](docs/CONFIGURATION) for a complete guide and documentation.

  1. Change hostname to your hostname.
    ```
    "HOSTNAME": "srv-your-hostname"
    ```

  2. Change the AWS S3 bucket name.
    ```
    "BUCKET_NAME": "cnbackup"
    ```

  3. Configure AWS CLI or AWS roles.

    * AWS CLI
      - Install - See [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

      - Configure - See [Quick Configuration](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)

    * AWS roles
      - See [IAM Roles for Amazon EC2](http://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)


* Execute Backup manually
```
$ python /path/to/backup.py -r -c /path/to/conf.json -l WARNING
```
* Optionally add a cronjob
```
$ crontab -e
00 03 * * * python /var/lib/nc-backup-py/backup.py -r -c /etc/nc-backup-py/conf.json
```

* Provide feedback on [Issue](https://github.com/ChinaNetCloud/nc-backup-py/issues) for suport,


## Features

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

## How to contribute

We appreciate all contributions and need and are looking forward for your help.

#### Developer:
1. Install the `test-dev` branch and get it to work.

2. Create an [Issue](https://github.com/ChinaNetCloud/nc-backup-py/issues) and start discussion providing as many details as possible, with maintainers team.

3. Once the issue is accepted you will be added to the team as contributor, then you can start development.

4. Commit to your own branch.

5. Send merge request to test test-dev once done with your feature and update on Issues.

6. Iterate :P.

*ChinaNetCloud/nc-backup-py is licensed under the
[Apache License 2.0](LICENSE)*
