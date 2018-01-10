
## Storage Configuration

All upload commands are run using templates at "nc-backup-py/storage/storage_templates.json".

Templates for local, oss, s3, scp and rsync are available in the package. It is possible to configure the script to run any bash command. See Custom Command Example below.

Multiple storage options can be configured into one.

### Local backup
```json
  "STORAGE_LOCAL": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION": "local",
      "TARGETS": "/opt/backup/encrypted",
      "ARGS_DICT": "{'LOCAL_BACKUP': '/opt/backup/local'}",
      "REMOVE_TARGETS": "True"
    }
  }
```

### AWS s3

Add the below section to `/etc/nc-backup-py/conf.json` and

See [Using Amazon S3](#using-amazon-s3) below for how to setup the 3rd party tool awscli.
```json
  "STORAGE_OSS": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"oss",
      "ACTION": "upload",
      "OBJECTIVES": "/opt/backup/encrypted",
      "ARGS_DICT": "{}",
      "__READTHIS": "Use alicmd -c to configure oss access and bucket.",
      "REMOVE_TARGETS": "False"
    }
},
```
This section is to store the backup, in this case s3. S3 is the only current backend implemented, but the script is supposed to support various backends including OSS, SSH, etc.

### Aliyun OSS

Add the below section to `/etc/nc-backup-py/conf.json` and

See [Using Aliyun Object Storage Services](#using-aliyun-object-storage-services) below for how to setup the 3rd party tool alicmd.

```json
  "STORAGE_OSS": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"oss",
      "ACTION": "upload",
      "OBJECTIVES": "/opt/backup/encrypted",
      "ARGS_DICT": "{}",
      "__READTHIS": "Use alicmd -c to configure oss access and bucket.",
      "REMOVE_TARGETS": "False"
    }
  },
```

### Customized storage

Customized storages can be defined using **Named placeholders** feature of python.

For example the `aws s3` cli command is defined as follows in the file [storage_templates.json](nc-backup-py/storage/storage_templates.json)

```json
  "UPLOAD_COMMAND_TEMPLATE": "aws s3 cp %(OBJECTIVES)s/%(file)s s3://%(BUCKET)s/%(HOSTNAME)s/%(file)s",
  "UPLOAD_COMMAND_DICT": "{'BUCKET': 'ncbackup'}",
```

Use UPLOAD_COMMAND_TEMPLATE to define your upload command and use UPLOAD_COMMAND_DICT to set variables.

Behind the hood, the shell command is created as follows.

```python
UPLOAD_COMMAND_DICT['HOSTNAME'] = HOSTNAME
UPLOAD_COMMAND_DICT['OBJECTIVES'] = OBJECTIVES

for file in os.listdir("OBJECTIVES")
  UPLOAD_COMMAND_DICT['file'] = "%s/file" % OBJECTIVES
  UPLOAD_COMMAND_TEMPLATE % UPLOAD_COMMAND_DICT
  ... execute command ...
```

For example, the `aws s3 cp` can be used as below to upload to ncbackup.

```json
"STORAGE_CUSTOM": {
  "ACTION": "execute",
  "NAME": "storage",
  "PARAMETERS":{
    "DESTINATION":"custom_command",
    "OBJECTIVES": "/opt/backup/encrypted",
    "UPLOAD_COMMAND_TEMPLATE": "aws s3 cp %(OBJECTIVES)s/%(file)s s3://%(BUCKET)s/%(HOSTNAME)s/%(file)s",
    "ARGS_DICT": "{'BUCKET': 'ncbackup'}",
    "__READTHIS": "Use UPLOAD_COMMAND_TEMPLATE to create your custom command.",
    "__READTHIS1": "ARGS_DICT to pass variables to your custom upload command",
    "REMOVE_TARGETS": "False"
    }
  },
```

### Combine storages

```json
  "STORAGE_S3": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"s3",
      "ACTION": "upload",
      "OBJECTIVES": "/opt/backup/encrypted",
      "ARGS_DICT": "{'BUCKET': 'ncbackup'}",
      "REMOVE_TARGETS": "False"
    }
  },
  "STORAGE_OSS": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION":"oss",
      "ACTION": "upload",
      "OBJECTIVES": "/opt/backup/encrypted",
      "ARGS_DICT": "{}",
      "__READTHIS": "Use alicmd -c to configure oss access and bucket.",
      "REMOVE_TARGETS": "False"
    }
  },
  "STORAGE_LOCAL": {
    "ACTION": "execute",
    "NAME": "storage",
    "PARAMETERS":{
      "DESTINATION": "local",
      "TARGETS": "/opt/backup/encrypted",
      "ARGS_DICT": "{'LOCAL_BACKUP': '/opt/backup/local'}",
      "REMOVE_TARGETS": "True"
    }
  }
```

## Setup 3rd party clients.

Instructions on how to setup 3rd party clients are given below.

### Using Amazon S3

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

### Using Aliyun Object Storage Services

  * To upload backups to Aliyun OSS install aliyun-oss-tools.
  aliyun-oss-tools

  * You may have to add CNC repo first:
    ```bash
    [root@localhost ~]# cat /etc/yum.repos.d/CNC.repo
    [cnc]
    name=cnc
    baseurl=http://repo.service.chinanetcloud.com/repo/el$releasever/base/$basearch/
    gpgcheck=1
    #gpgkey=http://61.129.13.40/repo/rpm-gpg/RPM-GPG-KEY-CNC
    gpgkey=http://repo.service.chinanetcloud.com/repo/rpm-gpg/RPM-GPG-KEY-CNC


    [cnc_devel]
    name=cnc_devel
    baseurl=http://repo.service.chinanetcloud.com/repo/el$releasever/devel/$basearch/
    gpgcheck=1
    enabled=0
    gpgkey=http://repo.service.chinanetcloud.com/repo/rpm-gpg/RPM-GPG-KEY-CNC
    ```

  * Install aliyun-oss-tools.
  `# yum install aliyun-oss-tools`

  * Add x privilege to command

  `# chmod a+x /usr/bin/alicmd`

  * Get help information

  `# alicmd -h`

  * Check if this files exist (/etc/.alioss.conf), if does not exist, proceed with configure AliYun OSS, else (if exist), remove the old config file

  `rm -rf /etc/.alioss.conf`

  * Configure AliYun OSS

    Before you configure, please make sure you check if this server can access Aliyun OSS using private address. The difference is that if the server can access Aliyun using private address the traffic is considered internal therefore it's FREE. If you use public addresses the customer is charged for this traffic. this amount is changed as per daily backup, so it could be a lot if there is a lot of information to backup.

  ```bash
  # alicmd --config
  You will see some contents like below
  [INFO]: Start to config AliYun Open Storage Service.
  [INFO]: Host 'storage.aliyun.com' selected automatically. You can also update file  /etc/alioss.conf manually. # Backup Host is determined automatically.
  Please input your ACCESS_ID:       # FIND THE ID/KEY in our keepass file(search OSS).
  Please input your ACCESS_KEY:
  Please input your bucket:        #Our default bucket is "chinanetcloud"
  Plase input CNC server name:
  [INFO]: AliYum OSS is configured sucessfully !
  [INFO]: Configuration file saved.`
  ```

  * Edit the alioss config file.
  ```bash
  vim /etc/.alioss.conf ;`
  [options]
  retry_times = 15
  multi-upload = on # if the backup file size is more than 100MB
  ```  

  * Verify OSS Configuration file:

  ```bash
  # alicmd --show
  XXcloud 2012-06-19T07:05:33.000Z  # Should list all buckets we have`
  ```

  * Check the backup files on Aliyun:

  `# alicmd -l`

  * Check from the console.
  URL: www.aliyun.com (username and password) Selete
  用户中心 --> 管理控制台 --> 开放存储服务OSS --> OSS 管理 --> OSS体验站`
