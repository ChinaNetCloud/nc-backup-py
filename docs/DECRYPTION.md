## How to decrypt

The encryption script `/var/lib/nc-backup-py/encryption/encryption.py` is also used for decryption.

### Decrypting a single file:

* The backup files are encrypted with keys located at `/etc/nc-backup-py/key_file`.

* Download the files to you computer (ex:`/opt/backup/restore`)
  ```bash
  $ mkdir -p /opt/backup/restore # If /opt/backup/restore is not present
  $ aws s3 cp s3://cnc-bj-backup/srv-nc-bj-zabbix-qa1/20160705_042923.tar.gz.crypt.000 /opt/backup/restore
  ```

* Restore using the following command. Here `20171106_105027.tar.gz` is the decrypted tar archive.
  ```bash
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

### Decrypting multiple files

* If the encrypted file has been split into multiple parts, point to the common name `20171106_105027.tar.gz.crypt`
  ```bash
  $ ls /opt/backup/restore
  20171106_105027.tar.gz.crypt.000
  20171106_105027.tar.gz.crypt.001
  20171106_105027.tar.gz.crypt.002
  20171106_105027.tar.gz.crypt.003
  ```

* Restore using the following command. Here `20171106_105027.tar.gz` is the decrypted tar archive.

  ```bash
  $ python /var/lib/nc-backup-py/encryption/encryption.py -d \
  --KEY_FILE "/etc/nc-backup-py/key_file" \
  --OBJECTIVES "20171106_105027.tar.gz.crypt" \ #
  --DESTINATION "20171106_105027.tar.gz" \
  --HOME_FOLDER "/var/lib/nc-backup-py"
  ```
  `20171106_105027.tar.gz.crypt` will match all 4 files in the above example.


  *Note: The only difference to decrypt one or more than one file is in the name of --OBJECTIVES. The first example show the whole path and the second example shows only the path with the part of the name that is common.*

* untar the file to your destination:

  ```bash
  $ tar -xvf $TAR_ARCHIVE $DEST_PATH
  $ tar -xvf 20160607_161750.tar.gz untared/
  $ ls untared/
  etc
  var
  ```

#### Upcoming feature:

A restore script that will take input interactively and decrypt files. It will be able to send a report on decryption to a preconfigured URL and email using POST and SMTP.
