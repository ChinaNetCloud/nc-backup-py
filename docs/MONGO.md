# MongoDB Dumps

* This feature is still in testing, please help us by testing and providing feedback.

We can execute mongoDB by adding the following configuration. It executes the external mongodump commnd.

* Add mogo section to configuration file and add `/opt/backup/mongodump` to `COMPRESSION.TARGETS`

```json
  "MONGODB":{
    "ACTION": "load",
    "FROM": "mongo",
    "FILENAME": "mongo",
    "CLASS": "MongoBackup",
    "PARAMETERS":{
      "MONGO_USER": "",
      "MONGO_PWD": "",
      "MONGO_HOST": "127.0.0.1",
      "MONGODUMP_BIN": "/usr/bin/mongodump",
      "TAR_COMMAND": "sudo /bin/tar czf",
      "PREFIX_FOLDER": "mongodump",
      "DESTINATION": "/opt/backup/mongodump"
    }
  },
    "COMPRESSION": {
    "ACTION": "execute",
    "NAME": "compression",
    "PARAMETERS": {
      "TARGETS": "/opt/backup/files /opt/backup/mongodump",
      "DESTINATION":"/opt/backup/compressed",
      "REMOVE_TARGETS": "True"
  }
  },    
```
