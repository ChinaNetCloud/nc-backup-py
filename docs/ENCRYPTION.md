# Encryption

```json
     "ENCRYPTION": {
        "ACTION": "execute",
        "NAME": "encryption",
        "PARAMETERS": {
          "KEY_FILE": "/etc/nc-backup-py/key_file",
          "FILE_SIZE": "100",
          "TARGETS": "/opt/backup/compressed",
          "DESTINATION":"/opt/backup/encrypted",
          "REMOVE_TARGETS": "True"
        }
    }
```

This section as the name indicates encrypts files, but also splits long files according to FILE_SIZE give in MB. "KEY_FILE" is the path to the key file.

Regarding the optional end required parameters the same could be exported to the encryption configuration so the minimal working configuration for a standard system is as follows:
```json
     "ENCRYPTION": {
        "ACTION": "execute",
        "NAME": "encryption"
    }
```
Notice: Out standard for the configurations has changed so now all the configuration files have to be in /etc/nc-backup-py/ in this case the key file will be in /etc/nc-backup-py/key_file.
