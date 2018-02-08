
# MySQL Backups

nc-backup-py can backup MySQL databases by making a mysqldump of the specified databases.

A sample configuration for MySQL is installed at [/etc/nc-backup-py/Examples/conf.mysql.json](nc-backup-py/conf/Examples/conf.mysql.json)

You can copy the above sample file or parts of the sample file and modify it to suit your needs.

Below is a sample mysql configuration section.

```JSON
"MYSQL": {
  "ACTION": "execute",
  "NAME": "mysql_backup",
  "EXECUTABLE": "mysql_dump.py",
  "PARAMETERS": {
    "CREDENTIAL_PATH": "/etc/nc-backup-py/mysql.credentials",
    "EXCLUDE_DB": "mysql performance_schema",
    "CONF_PATH": "/etc/my.cnf",
    "EXCLUDE_TABLE": "",
    "BINLOG_DAYS": 1
  }
}
```

## MYSQL parameters:

`CREDENTIAL_PATH` - This is to specify the path to the MySQL credentials file. We will consider using the same Variable Name for other database systems.
`CONF_PATH` - This if for the path to MySQL my.cnf file (Common location: /etc/my.cnf or /etc/mysql/my.cnf or /var/lib/data/my.cnf).
`DATA_DIR` - MySQL data directory, (Common location: /var/lib/mysql/data)
`MY_INSTANCES` - List space separated ports for the different instances running on a server default: "3306",
`BINLOG_PATH` - Path to binary logs for MySQL.
`BINLOG_FILE_PREFIX` - This is the beginning of the name normally defined my.cnf
`MYSQL_DUMP_BINARY` - Path to mysqldump binary executable file.
`MYSQL_BINARY` - Path to MySQL binary executable file.
`PREFIX_FOLDER` - Name of the folder and file prefix for MySQL backups inside the WORK_FOLDER.
`EXCLUDE_DB` - Database name to exclude.
`EXCLUDE_TABLE` Database and table names to exclude separated by a "." follow standard SQL notation e.g.: "mysql.user mysql.func mysql.event"
`BINLOG_DAYS` - Number of days of bin-logs to take.
