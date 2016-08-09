import os
import shutil
import pwd
import grp


from execution.config_parser import ConfigParser

# Check that the script is running as root.
if os.geteuid() != 0:
    print "Error: The installer needs to be executed as superadmin"
    exit(1)

# Create ncbackup if it does not exists.
username = 'ncbackup'

# try:
#     pwd.getpwnam(username)
#     print username + ' user already exists.'
# except KeyError:
#     print 'User ' + username + ' does not exist. Adding it now'
os.system('useradd -m %s -s /sbin/nologin' % username)


print 'Copy configs...'
# Copy the files function
def copy_files(source, destination, username):
    # Os chown of the config folder
    """
    :rtype: object
    """
    uid = pwd.getpwnam(username).pw_uid
    gid = grp.getgrnam(username).gr_gid
    files = os.listdir(source)
    files.sort()
    os.chown(destination, uid, gid)
    for f in files:
        src = source + '/' + f
        dst = destination + '/' + f
        if os.path.isdir(src) == True:
            try:
                os.stat(dst)
                os.chown(dst, uid, gid)
            except:
                os.mkdir(dst)
                os.chown(dst, uid, gid)
        else:
            shutil.copy(src, dst)
            os.chown(dst, uid, gid)

# Current folder
path = os.getcwd()
path_with_conf = path + '/conf'

# Move default config files to /etc.
configs_path = '/etc/nc-backup-py'
try:
    os.stat(configs_path)
except:
    os.mkdir(configs_path)
# Copy the configs to /etc
copy_files(path_with_conf, configs_path, username)

# Copy code to var/lib
destination_code_path = '/var/lib/nc-backup-py'
try:
    os.stat(destination_code_path)
except:
    os.mkdir(destination_code_path)
# Copy files...
copy_files(path, destination_code_path, username)

uid = pwd.getpwnam(username).pw_uid
gid = grp.getgrnam(username).gr_gid

# Logs path
logs_path = '/var/log/nc-backup-py'
try:
    os.stat(logs_path)
except:
    os.mkdir(logs_path)

os.chown(logs_path, uid, gid)


# Backup folder
backup_path = '/opt/backup'
try:
    os.stat(backup_path)
except:
    os.mkdir(backup_path)

os.chown(backup_path, uid, gid)