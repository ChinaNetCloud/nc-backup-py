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
import socket

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
                logging.warn(e)
        for name in files:
            dst_root = root.replace(src, dst)
            try:
                shutil.copyfile(os.path.join(root, name),
                                os.path.join(dst_root, name))
                os.chown(os.path.join(dst_root, name), uid, gid)
            except shutil.Error:
                logging.warn(e)


def sed(filename, pattern, replacement):
    """Replace pattern with replacement in a file."""
    import re
    with open(filename, "r") as sources:
        lines = sources.readlines()
    with open(filename, "w") as sources:
        for line in lines:
            sources.write(re.sub(pattern, replacement, line))


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
            os.chown(LOGS_PATH, uid, gid)

        except OSError:
            logging.info("The path %s already exists." % LOGS_PATH)
        os.chown(LOGS_PATH, uid, gid)

        # Backup folder
        logging.info('************************************')
        logging.info('* Creating backup folder on ' + BACKUP_PATH + '...')
        logging.info('************************************')
        try:
            os.mkdir(BACKUP_PATH)
            os.chown(BACKUP_PATH, uid, gid)
        except:
            logging.warning("The path %s already exists." % BACKUP_PATH)
        os.chown(BACKUP_PATH, uid, gid)

        # Copy config template
        logging.info('************************************')
        logging.info('* Copy configs...')
        logging.info('************************************')
        try:
            os.mkdir(CONFIG_PATH)
            os.chown(CONFIG_PATH, uid, gid)
        except:
            logging.warning("The path %s already exists." % CONFIG_PATH)
        copy_files('nc-backup-py/conf', CONFIG_PATH, uid=uid, gid=gid)

        # Get hostname
        hostname = socket.gethostname()
        # Change hostname and create default configuration template.
        for filename in os.listdir(os.path.join(CONFIG_PATH, "Examples")):
            print "filename: %s" % filename
            sed(os.path.join(CONFIG_PATH, "Examples", filename), r"srv-nc-template-host-config", hostname)
        ######
        with open(os.path.join(CONFIG_PATH, "Examples", filename), "r") as sources:
            lines = sources.readlines()
            for line in lines:
                if "HOSTNAME" in line:
                    print line
        # Copy s3 backup as default config
        sample = os.path.join(CONFIG_PATH, "Examples/conf.s3.json")
        default = os.path.join(CONFIG_PATH, "conf.json")
        print sample
        print default
        logging.info("Copy default config from %s to %s" % (sample, default))
        copy_files(sample, default, uid=uid, gid=gid)
        sed(os.path.join(CONFIG_PATH, "conf.json"), r"srv-nc-template-host-config", hostname)

        # Copy src
        logging.info('************************************')
        logging.info('* Copy nc-backup-py to %s...' % DEST_PATH)
        logging.info('************************************')
        try:
            os.mkdir(DEST_PATH)
            os.chown(DEST_PATH, uid, gid)
        except:
            logging.warning("The path %s already exists." % DEST_PATH)
        copy_files('nc-backup-py', DEST_PATH, uid=uid, gid=gid)


setup_package()
