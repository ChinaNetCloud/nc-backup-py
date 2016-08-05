import os
import pwd
from shutil import move


from execution.config_parser import ConfigParser

# Check that the script is running as root.
if os.geteuid() != 0:
    print "Error: The installer needs to be executed as superadmin"
    exit(1)

# Create ncbackup if it does not exists.
username = 'ncbackup'

try:
    pwd.getpwnam(username)
    print username + ' already exists.'
except KeyError:
    print 'User ' + username + ' does not exist. Adding it now'
    os.system('useradd -m %s -s /sbin/nologin' % username)

# Move default config files to /etc.
configs_path = '/etc/nc-backup-py'
if not ConfigParser.check_exists(ConfigParser(),configs_path):
    move(os.getcwd() + '/conf/.', configs_path)
else:
    move(os.getcwd() + '/conf/.', configs_path + '.')

# make ncbackup the owner of /etc folder.




