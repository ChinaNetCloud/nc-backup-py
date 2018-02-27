# PostgreSQL

* This feature is still in testing, please help us by testing and providing feedback.

Create backup user ncbackup in postgresql

`postgres=> create user ncbackup with password 'PASSWORD';`

Details about how to create user in pgsql, please refer to Basic postgresql management procedure

`Grant select privilege on all user_created tables to ncbackup
Customerdb=> grant select on $TABLE_NAME to ncbackup;`

You have to grant privilege one by one, of cource, you could also create a batch scipt to do it.

Create `.pgpass` file in `/home/ncbackup` with following contents, that is for backup script authenticaiton.
`localhost:*:*:ncbackup:$PASSWORD`
You should change the `$PASSWORD` part accordingly

Setup ownership and privilge like the following:

```
[root@srv-xxx-xxx ~]# ls -l /home/ncbackup/.pgpass
-rw------- 1 ncbackup ncbackup 34 Jun 12 17:04 /home/ncbackup/.pgpass
```

Be careful, `600` permisions is a must when the backup will be restored, before you do anything, you must create all the user and database related to the backup, or the restore will fail

## Sample Configuration snippet
```json
     "POSTGRES":{
        "ACTION": "load",
        "FROM": "postgres",
        "FILENAME": "postgres",
        "CLASS": "PostgresBackup",
        "PARAMETERS": {
          "PREFIX_FOLDER": "pgdump",
          "PSQLDUMP": "/usr/bin/pg_dump",
          "PSQL": "/usr/bin/psql",
          "DESTINATION": "/opt/backup",
          "EXCLUDE_DB": ""
        }
    }
```
