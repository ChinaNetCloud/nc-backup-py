
## Using Amazon S3

  * AWS CLI

    - Install - See [Installing the AWS Command Line Interface](http://docs.aws.amazon.com/cli/latest/userguide/installing.html)

    - Configure - See [Quick Configuration](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html#cli-quick-configuration)

    - Please switch user to `ncbackup` before configuring AWS CLI
      ```
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

## Using Aliyun Object Storage Services

  * To upload backups to Aliyun OSS install aliyun-oss-tools.
  aliyun-oss-tools

  `# yum install aliyun-oss-tools`

  * Add x privilege to command

  `# chmod a+x /usr/bin/alicmd`

  * Get help information

  `# alicmd -h`

  * Check if this files exist (/etc/.alioss.conf), if does not exist, proceed with configure AliYun OSS, else (if exist), remove the old config file

  `rm -rf /etc/.alioss.conf`

  * Configure AliYun OSS

    Before you configure, please make sure you check if this server can access Aliyun OSS using private address. The difference is that if the server can access Aliyun using private address the traffic is considered internal therefore it's FREE. If you use public addresses the customer is charged for this traffic. this amount is changed as per daily backup, so it could be a lot if there is a lot of information to backup.

  ```
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
  ```
  vim /etc/.alioss.conf ;`
  [options]
  retry_times = 15
  multi-upload = on # if the backup file size is more than 100MB
  ```  

  * Verify OSS Configuration file:

  ```
  # alicmd --show
  XXcloud 2012-06-19T07:05:33.000Z  # Should list all buckets we have`
  ```

  * Check the backup files on Aliyun:

  `# alicmd -l`

  * Check from the console.
  URL: www.aliyun.com (username and password) Selete
  用户中心 --> 管理控制台 --> 开放存储服务OSS --> OSS 管理 --> OSS体验站`
