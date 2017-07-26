#!/usr/bin/env python2
"""Setup nc-backup-py."""

import os
import pwd
import grp
import sys
import shutil
import logging
from setuptools import setup
from setuptools.command.install import install


if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    PYTHON_MODULE_REQUIREMENTS = [
        'requests',
        'pycrypto',
        'awscli'
    ]

elif sys.version_info[0] == 2 and sys.version_info[1] == 6:
    PYTHON_MODULE_REQUIREMENTS = [
        'requests',
        'simplejson',
        'backport_collections',
        'awscli'
    ]

PYTHON_REQUIREMENTS = '>=2.6,<3.0'
BACKUP_USERNAME = 'ncbackup'
# EXECUTABLE = {
#     'console_scripts': [
#         'nc-backup-py = nc_backup_py.backup',
#     ]
# }

CONFIG_PATH = '/etc/nc-backup-py'
BACKUP_PATH = '/opt/backup'
LOGS_PATH = '/var/log/nc-backup-py'
DEST_PATH = '/var/lib/nc-backup-py'


def check_superuser():
    """Check if setup was run as root."""
    if os.geteuid() != 0:
        logging.error("Execute pip install as root.")
        exit(1)


def create_user(username):
    """Create user if it does not exists."""
    try:
        pwd.getpwnam(username)
        logging.warning('The user  %s already exists. Not creating' % username)
    except KeyError:
        os.system('useradd -m %s -s /sbin/nologin' % username)
        logging.info('Done.')


def copy_files(src, dst, uid, gid):
    """Copy files recursively and set uid and gid."""
    for root, dirs, files in os.walk(src):

        for name in dirs:
            dst_root = root.replace(src, dst)
            try:
                logging.warning("%s|%s" % (dst_root, name))
                logging.warning(os.path.join(root, name))
                os.mkdir(os.path.join(dst_root, name))
                os.chown(os.path.join(dst_root, name), uid, gid)
            except OSError, e:
                print e
        for name in files:
            dst_root = root.replace(src, dst)
            try:
                shutil.copyfile(os.path.join(root, name),
                                os.path.join(dst_root, name))
                os.chown(os.path.join(dst_root, name), uid, gid)
            except shutil.Error:
                pass


def setup_package():
    """Setup package."""
    setup(name='nc-backup-py',
          version='0.1',
          description='A comprehensive one stop solution for backups.',
          url='https://github.com/ChinaNetCloud/nc-backup-py',
          author='China Net Cloud',
          author_email='raghulmz@gmail.com',
          license='Apache 2.0',
        #   packages=['nc_backup_py'],
          install_requires=PYTHON_MODULE_REQUIREMENTS,
          python_requires=PYTHON_REQUIREMENTS,
          cmdclass={'install': Setup_nc_backup_py},
        #   include_package_data=True,
        #   entry_points=EXECUTABLE,
          zip_safe=False)


class Setup_nc_backup_py(install):
    """Install nc-backup-py"""

    def run(self):
        """Install nc-backup-py and run postinstall."""
        install.run(self)
        check_superuser()
        logging.info('************************************')
        logging.info('* Creating ' + BACKUP_USERNAME + ' user...')
        logging.info('************************************')
        create_user(BACKUP_USERNAME)

        # Copy sudoers file for ncbackup
        shutil.copy(src="nc-backup-py/sudoers.d/ncbackup",
                    dst="/etc/sudoers.d/")
        os.chown("/etc/sudoers.d/ncbackup", 0, 0)
        os.chmod("/etc/sudoers.d/ncbackup", 0644)

        # Get uid and gid of BACKUP_USERNAME
        uid = pwd.getpwnam(BACKUP_USERNAME).pw_uid
        gid = grp.getgrnam(BACKUP_USERNAME).gr_gid

        # Logs path
        logging.info('************************************')
        logging.info('* Creating log folder on ' + LOGS_PATH + '...')
        logging.info('************************************')
        try:
            os.mkdir(LOGS_PATH)
        except OSError:
            logging.info("The path %s already exists." % LOGS_PATH)
        os.chown(LOGS_PATH, uid, gid)

        # Backup folder
        logging.info('************************************')
        logging.info('* Creating backup folder on ' + BACKUP_PATH + '...')
        logging.info('************************************')
        try:
            os.mkdir(BACKUP_PATH)
        except:
            logging.warning("The path %s already exists." % BACKUP_PATH)
        os.chown(BACKUP_PATH, uid, gid)

        # Copy config template
        logging.info('************************************')
        logging.info('* Copy configs...')
        logging.info('************************************')
        copy_files('nc-backup-py/conf', CONFIG_PATH, uid=uid, gid=gid)

        # Copy src
        logging.info('************************************')
        logging.info('* Copy nc-backup-py to %s...' % DEST_PATH)
        logging.info('************************************')
        copy_files('nc-backup-py', DEST_PATH, uid=uid, gid=gid)


setup_package()
