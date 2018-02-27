# MongoDB Dumps

* This feature is still in testing, please help us by testing and providing feedback.

We can execute mongoDB by adding the following configuration. It executes the external mongodump commnd.

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
          "DESTINATION": "/opt/backup"
        }
    }    
```
