# COMPRESSION

This section takes a set of folders and compresses them. The parameters "REMOVE_TARGETS": "True" means that the script will remove the fileset passed as parameters. We are discussing the possibility of changing "OBJECTIVES" in all sections to some other candidate word like FILESETS. If this change is finally implemented the development changes are not a lot. Compression also has many optional parameters, so in a standard CentOS 6 or 7 configuration this configuration could look like this:

```json
     "COMPRESSION": {
        "ACTION": "execute",
        "NAME": "compression",
        "PARAMETERS": {
          "TARGETS": "/opt/backup/files /opt/backup/mongodump"
        }
    }
```

The system will assume on it's own the default values as per the first compression configuration sample. You only need to change it if your parameters NEED to be different, even when we would not advise it unless strictly required.

# Sample section

```json
     "COMPRESSION": {
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
    }
```
