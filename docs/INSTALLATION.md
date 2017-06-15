# Installation


## installation

This is the installation manual for nc-backup-py (Net Could Backups) system currently in testing and development phase as wel as used for some productions systems.

## Required Skills

Understand basics about JSON format.
Linux commands and packages installation.

## Quick setup (Quick Start Procedure)

This quick setup guide is to install ONLY our default filesbackup configuration (/etc /opt/ncscripts /var/spool/cron) and upload to AWS S3. Before you start, please make sure you have the requirements installed.

### Download the script to the server

Let's use your home folder of a sudoer user as download folder:

`
[abel.guzman@xxx] cd ~

[~]$ git clone https://gitlab.service.chinanetcloud.com/backup/nc-backup-py.git
`
### Use setup.py file to create user and other required tasks

Execute the file called setup.py in the nc-backup-py folder. This file executes automatically all the following tasks until configuration. The configuration will need to be done by you manually or using other method. To execute get in the git cloned directory and execute:

`# python setup.py`

This step should work correctly, if it does you can skip the following sub-section called "Create user to run backup with out using the `setup.py`":

#### Create user to run backup with out using the setup.py

Create basic folders structure and move files. To be sure it worked or not you just need to check the files en folder in the two steps to be at the right place and with the right permissions.

##### Create user to run backup:

`[~]$ sudo useradd -m ncbackup -s /sbin/nologin`

##### Create basic folders structure and move files
`[~]$ sudo mkdir /etc/nc-backup-py/`

##### Move the default configuration file from where the you downloaded to /etc/nc-backup-py/ and make ncbackup the owner e.g.:.

`
[~]$ sudo mv ~/nc-backup-py/conf/* /etc/nc-backup-py/

[~]$ sudo chown ncbackup:ncbackup /etc/nc-backup-py/ -R
`

##### Create log folder:

`[~]$ sudo  mkdir /var/log/nc-backup-py/
[~]$ sudo  chown ncbackup:ncbackup -R /var/log/nc-backup-py/`

##### Create code deployment directory, move code and make ncbackup the owner:

`[~]$ sudo mv ~/nc-backup-py/ /var/lib/

[~]$ sudo chown ncbackup:ncbackup -R /var/lib/nc-backup-py/`

##### Create default backup folder:

`[~]$ sudo mkdir /opt/backup/

[~]$ sudo chown ncbackup:ncbackup -R /opt/backup/`
