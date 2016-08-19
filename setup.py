import os
import shutil
import pwd
import grp
import sys


##################
# Pre-run Checks #
##################
# Check that the script is running as root.
print '************************************'
print '* General Cheks'
print '************************************'
if os.geteuid() != 0:
    print "Error: The installer needs to be executed as superadmin"
    exit(1)
print 'Done.'
#########################
# Software Requirements #
#########################
print '************************************'
print '* Software Requirements'
print '************************************'
try:
    import requests
    print 'Requests present.'
except ImportError:
    print 'Error Importing "requests", this library is required'
    exit(1)


python_version = '2.7'
if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    python_version = '2.7'
    try:
        from Crypto import Random
        print 'Crypto.Ramdom present'
    except ImportError:
        print 'Error importing Ramdom from Crypto, this library is required for Python 2.7'
        exit(1)
    try:
        from hashlib import md5
        print 'hashlib.md5 present'
    except ImportError:
        print 'Error importing md5 from hashlib, this library is required for Python 2.7'
        exit(1)
    try:
        from Crypto.Cipher import AES
        print 'Crypto.Cipher.AES present'
    except ImportError:
        print 'Error importing AES from Crypto.Cypher, this library is required for Python 2.7'
        exit(1)
elif sys.version_info[0] == 2 and sys.version_info[1] < 7 and sys.version_info[1] > 5:
    python_version = '2.6'
    try:
        import simplejson
        print 'Simplejson present'
    except ImportError:
        print 'Error importing simplejson, this library is required for Python 2.7'
        exit(1)
    try:
        from backport_collections import OrderedDict
        print 'backport_collections.OrderedDict present'
    except ImportError:
        print 'Error importing md5 from hashlib, this library is required for Python 2.7'
        exit(1)
else:
    print 'Unsupported python version, you are on your own'
    python_version = 'Unsupported'
print 'Done.'
#################################
# Copy files & user permissions #
#################################

# Create ncbackup if it does not exists.
username = 'ncbackup'
print '************************************'
print '* Creating ' + username + ' user...'
print '************************************'
try:
    pwd.getpwnam(username)
    print 'The user already exists; no need to create it'
except KeyError:
    os.system('useradd -m %s -s /sbin/nologin' % username)
    print 'Done.'

# Copy the files function
def copy_files(source, destination, username, space=''):
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
            print space + '- ' + src
            try:
                os.stat(dst)
                os.chown(dst, uid, gid)
            except:
                os.mkdir(dst)
                os.chown(dst, uid, gid)
            copy_files(src, dst, username, '  ')
        else:
            # print space + '|__' + src
            shutil.copy(src, dst)
            os.chown(dst, uid, gid)

# Current folder
path = os.getcwd()
path_with_conf = path + '/conf'
print 'Done.'

# Move default config files to /etc.
configs_path = '/etc/nc-backup-py'
print '************************************'
print '* Copy configs...'
print '************************************'
try:
    os.stat(configs_path)
except:
    os.mkdir(configs_path)
# Copy the configs to /etc
copy_files(path_with_conf, configs_path, username)
print 'Done.'
# Copy code to var/lib
destination_code_path = '/var/lib/nc-backup-py'
print '************************************'
print '* Copying installer to ' + destination_code_path + '...'
print '************************************'
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
print '************************************'
print '* Creating log foldel on ' + logs_path + '...'
print '************************************'
try:
    os.stat(logs_path)
except:
    os.mkdir(logs_path)
os.chown(logs_path, uid, gid)


# Backup folder
backup_path = '/opt/backup'
print '************************************'
print '* Creating backup folder on ' + backup_path + '...'
print '************************************'
try:
    os.stat(backup_path)
except:
    os.mkdir(backup_path)

os.chown(backup_path, uid, gid)