## How to decrypt

###if the server doing backups has python 2.7

The encryption script `/var/lib/nc-backup-py/encryption/encryption.py` is the same script used for decryption.

Example for a single file:

Download the files to /opt/backup/restore e.g.:
```
$ mkdir -p /opt/backup/restore # If /opt/backup/restore is not present
$ aws s3 cp s3://cnc-bj-backup/srv-nc-bj-zabbix-qa1/20160705_042923.tar.gz.crypt.000 /opt/backup/restore
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


If the encrypted file has been split into multiple parts, point to the common name `20171106_105027.tar.gz.crypt`

`20171106_105027.tar.gz.crypt` will match all 4 files in the below example.

```
$ ls /opt/backup/restore
20171106_105027.tar.gz.crypt.000
20171106_105027.tar.gz.crypt.001
20171106_105027.tar.gz.crypt.002
20171106_105027.tar.gz.crypt.003
$ python /var/lib/nc-backup-py/encryption/encryption.py -d \
--KEY_FILE "/etc/nc-backup-py/key_file" \
--OBJECTIVES "20171106_105027.tar.gz.crypt" \ #
--DESTINATION "20171106_105027.tar.gz" \
--HOME_FOLDER "/var/lib/nc-backup-py"
```

Notice: The only difference to decrypt one or more than one file is in the name of --OBJECTIVES. The first example show the whole path and the second example shows only the path with the part of the name that is common.

After this you have to untar the file using something like this:

`tar -xvf /opt/backup/20160607_161750.tar.gz /opt/backup/`

Idea: We might want develop a feature in the near future called "restore" that would do all the work for you and give you back the files already decompressed. This feature could even log information to BRT about the Restore job, and use dates, etc
