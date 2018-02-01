# Installation

This is the complete installation manual for nc-backup-py (Net Could Backups) system.

It give a detailed picture of what happens when setup.py is run. This can be used to troubleshoot installation problems.

## Required Skills

Understand basics about JSON format.
Linux commands and packages installation.

## Quick setup (Quick Start Procedure)

This quick setup guide is to install ONLY our default filesbackup configuration (/etc /opt/ncscripts /var/spool/cron) and upload to AWS S3. Before you start, please make sure you have the requirements installed.

Download or clone the repository into the home folder of an user with sudo privileges.




* Clone the script.
```
$ cd ~
$ git clone https://gitlab.service.chinanetcloud.com/backup/nc-backup-py.git
```
***or***

* Download the script.
```
$ wget -O nc-backup-py.zip https://github.com/ChinaNetCloud/nc-backup-py/archive/master.zip
$ unzip nc-backup-py.zip
$ cd nc-backup-py-master
```

* Use setup.py file to create user and other required tasks

Execute the file called setup.py in the nc-backup-py folder. This file executes automatically all the following tasks until configuration. The configuration will need to be done by you manually or using other method. To execute get in the git cloned directory and execute:

```
$ cd nc-backup-py
$ sudo python setup.py`
```

This step should work correctly, if it does you can move on to [CONFIGURATION](docs/CONFIGURATION.md)

### Python modules

Note: These modules come installed with most versions of Red Hat based distributions, you can try to execute the backups systems and if they are not present then install manually. If the modules required are not present the wscript will fail and inform about the name of the required modules. You can use yum search for looking for the binary installers if wanted or pip to install them.
You might need to enable epel repo if not enabled to install some modules:

`$ wget https://dl.fedoraproject.org/pub/epel/epel-release-latest-6.noarch.rpm
$ sudo rpm -iUvh epel-release-latest-6.noarch.rpm`

requests (could be installed with pip if not present: 'pip install requests' or using yum as well)
CentOS 7 and 6
`sudo yum install python-requests.noarch`
Crypto (Only for python 2.7)
CentOS 7
`sudo yum install python-crypto.x86_64`
CentOS 6
`sudo yum install python-crypto2.6.x86_64`
argparse
simplejson (Only for python 2.6)
`$ sudo yum install python-simplejson.x86_64`
backport_collections (Only for python 2.6)
`pip install backport_collections`


#### Create user to run backup with out using the setup.py

Create basic folders structure and move files. To be sure it worked or not you just need to check the files en folder in the two steps to be at the right place and with the right permissions.

* Create user to run backup:
```
$ sudo useradd -m ncbackup -s /sbin/nologin
```
* Create basic folders structure and move files
```
$ sudo mkdir /etc/nc-backup-py/
```

* Move the default configuration file from where the you downloaded to /etc/nc-backup-py/ and make ncbackup the owner e.g.:.
```
$ sudo mv ~/nc-backup-py/conf/* /etc/nc-backup-py/
$ sudo chown ncbackup:ncbackup /etc/nc-backup-py/ -R
```

* Create log folder:
```
$ sudo  mkdir /var/log/nc-backup-py/
$ sudo  chown ncbackup:ncbackup -R /var/log/nc-backup-py/`
```

* Create code deployment directory, move code and make ncbackup the owner:
```
$ sudo mv ~/nc-backup-py/ /var/lib/
$ sudo chown ncbackup:ncbackup -R /var/lib/nc-backup-py/`
```

* Create default backup folder:
```
$ sudo mkdir /opt/backup/
$ sudo chown ncbackup:ncbackup -R /opt/backup/`
```
