#!/usr/bin/env python2
"""Setup nc-backup-py."""

import os
import pwd
import grp
import sys
import shutil
import logging
from setuptools import setup
import site

if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    PYTHON_MODULE_REQUIREMENTS = [
        'Crypto',
        'hashlib',
        'awscli'
    ]

elif sys.version_info[0] == 2 and sys.version_info[1] == 6:
    PYTHON_MODULE_REQUIREMENTS = [
        'simplejson',
        'backport_collections',
        'awscli'
    ]

PYTHON_REQUIREMENTS = '>=2.6,<3.0'
BACKUP_USERNAME = 'ncbackup'
EXECUTABLE = {
    'console_scripts': [
        'nc-backup-py = src.backup',
    ]
}

CONFIG_PATH = '/etc/nc-backup-py'
BACKUP_PATH = '/opt/backup'
LOGS_PATH = '/var/log/nc-backup-py'
SCRIPT_HOME = '/var/lib/nc-backup-py'


def check_superuser():
    """Check if setup was run as root."""
    if os.geteuid() != 0:
        logging.error("Execute pip install as root.")
        exit(1)


def setup_package():
    """Setup package."""
    setup(name='nc-backup-py',
          version='0.1',
          description='A comprehensive one stop solution for backups.',
          url='https://github.com/ChinaNetCloud/nc-backup-py',
          author='China Net Cloud',
          author_email='raghulmz@gmail.com',
          license='Apache 2.0',
          packages=['src'],
          install_requires=PYTHON_MODULE_REQUIREMENTS,
          python_requires=PYTHON_REQUIREMENTS,
          include_package_data=True,
          entry_points=EXECUTABLE,
          zip_safe=False)


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
    try:
        shutil.copytree(src, dst)
    except OSError:
        logging.warning("The path %s already exists." % dst)
        logging.warning("The default files are not copied.")
    else:
        for root, dirs, files in os.walk(dst):
            for name in dirs:
                os.chown(os.path.join(root, name), uid, gid)
            for name in files:
                os.chown(os.path.join(root, name), uid, gid)


if __name__ == "__main__":

    check_superuser()
    setup_package()

    logging.info('************************************')
    logging.info('* Creating ' + BACKUP_USERNAME + ' user...')
    logging.info('************************************')
    create_user(BACKUP_USERNAME)

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

    copy_files('src/conf', CONFIG_PATH, uid=uid, gid=gid)

    print site.getsitepackages()
