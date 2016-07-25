import os
from shutil import move



# Check that the script is running as root.
if os.geteuid() != 0:
    print "Error: This installer needs to be executed by root"
    exit(1)

# Create ncbackup if it does not exists.
username = 'ncbackup'
os.system("useradd -m %s -s /sbin/nologin" % username)


move(os.getcwd() + '/conf/.', "/etc/nc-backup-py/")

# os.chdir(os.path.dirname(__file__))
# print(os.getcwd())


