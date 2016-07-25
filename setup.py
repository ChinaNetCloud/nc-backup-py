import os
from shutil import move


from execution.config_parser import ConfigParser

# Check that the script is running as root.
if os.geteuid() != 0:
    print "Error: This installer needs to be executed by root"
    exit(1)

# Create ncbackup if it does not exists.
username = 'ncbackup'
os.system("useradd -m %s -s /sbin/nologin" % username)

# Move default config files to /etc.
configs_path = '/etc/nc-backup-py'
if not ConfigParser.check_exists(ConfigParser(),configs_path):
    move(os.getcwd() + '/conf/.', configs_path)
else:
    move(os.getcwd() + '/conf/.', configs_path + '.')


# make ncbackup the owner of /etc folder.




