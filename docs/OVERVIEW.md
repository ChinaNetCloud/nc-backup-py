# OVERVIEW of nc-backup-py

In general nc-backup-py works similar to many backups systems but it's objectives are to achieve cloud and linux servers backups. Let's get into it for you to start getting familiar with it.

Notice: If you are interested on leaning about the structure of the project go ahead and read the rest of the introduction, but you do not really need this information to be able to install the software. In that case you can jump straight to Quick setup; manual install (Quick Start Procedure) or installation instructions and try to follow them.

Let's start explaining with execution. The project has a main script that is executed by calling the following command:

`python /path/to/backup.py -r -c /path/to/conf.json -l WARNING`

This command is able to perform all the backup tasks in sequential order according to the conf/conf.json configuration file order. As you might have already noticed nc-backup-py is developed using python and the configuration file is a JSON file. One of the main ideas behind the new software is to decouple code from configuration completely, so if at some point you find that you have to modify code then there is a bug in the system and it needs to be taken care of, we appreciate if you report it as an issue.
