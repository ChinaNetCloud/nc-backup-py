#!/usr/bin/python
"""

Get list of full volumes from the bacula database, upload the volumes
to S3, delete the volumes from the local system.

Tracy Reed
March 15, 2007

"""

import mimetypes
import os.path
import sys
import MySQLdb
import bitbucket
import time
import fcntl

AWS_ACCESS_KEY_ID = 'myaccesskey'
AWS_SECRET_ACCESS_KEY = 'mysecretkey'
BUCKET_NAME = 'mybucket'
BACKUP_DIR = '/home/treed/media/backups'

def daemonlock(progname, timeout=2):

    """Test lock for daemons to prevent multiple instances

    @param progname: The name of the caller. This name is used for the lock and
        should be unique on the system. Alternatively, this may be an absolute
        path for the lock file, which is useful for programs that do not run
        as root.
    @param timeout: Seconds to wait for the lock.
    @return:
         0 - success
        -1 - another daemon is still active
        -2 - some other error

    The lock will be released when the caller terminates. No unlock is
    required.

    This is much slicker than the old way of writing our pid out to a
    file and then reading in that file and parsing ps output to see if
    that pid still exists.
    """

    if progname.startswith(os.path.sep):
        lockfile = progname
    else:
        lockfile = "/var/run/%s.pid" % (progname.replace(os.path.sep, "_"))

    try:
        fd = os.open(lockfile, os.O_CREAT | os.O_RDWR, 0644)
    except OSError, e:
        print e
        return -2

    timed_out = True              # Assume failure
    t_end = time.time() + timeout
    while time.time() < t_end:
        try:
            fcntl.lockf(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            timed_out = False
            break
        except IOError, e:
            pass
        time.sleep(0.3)         # Wait a little to minimise CPU load

    if timed_out:
        return -1
    else:
        # Got lock, write the program's current pid
        os.write(fd, "%d\n" % (os.getpid()))
        return 0

def get_full_volumes():

    """ Connect to the database and get a list of all of the full
    volumes. Return the list. """

    db = MySQLdb.connect(host="localhost", user="root", passwd="mypassword", db="bacula")
    cursor = db.cursor()
    cursor.execute("select VolumeName from Media where VolStatus='Full'")
    result = cursor.fetchall()
    return result

def upload_volumes(full_volumes):

    """ Use bitbucket to establish a connection to S3. Iterate over
    full_volumes and upload each one.  Bitbucket is cool in that it
    makes the files to upload keys in a dictionary. The bucket is the
    dictionary, the keys are the files, the values associated with the
    keys are the contents. So to put data into file on S3 we just
    assign the data to a key and it gets uploaded. It automatically
    checks if the contents are the same using md5sum in the
    implementation of the bucket object and if they are the same
    already it does not upload the data.  """

    connection = bitbucket.connect(access_key=AWS_ACCESS_KEY_ID, secret_key=AWS_SECRET_ACCESS_KEY)
    bucket = connection.get_bucket(BUCKET_NAME)
    for record in full_volumes:
        file=("%s/%s" % (BACKUP_DIR, record[0]))
        print file
        if os.path.exists(file):

            # This while causes us to loop which retries the
            # upload. We increment attempts each time through and if
            # attempts is less than 3 we raise ValueError which gets
            # caught with a pass which causes us to hit the bottom of
            # the loop so we start over. If attempts is 3 or greater
            # we don't raise ValueError which causes us to hit the
            # else clause which contains a break which gets us out of
            # the loop.

            attempts = 0
            while 1:
                # This try for implementing the retry mechanism
                try:

                    # This try for ignoring empty files
                    try:
                        if bucket.has_key(record[0]):
                            bits = bucket[record[0]]
                            bits.filename = file
                        else:
                            bits = bitbucket.Bits(filename=file)
                            # Here's where we assign bits (read in
                            # from the file) to record[0] (the
                            # filename in S3) to a key in the bucket.
                            bucket[record[0]] = bits
                        os.unlink("%s/%s" % (BACKUP_DIR, record[0]))
                    except bitbucket.BitBucketEmptyError:
                        print 'sync_dir: Empty File - Ignored %s' % fullpath
                    attempts = attempts + 1
                    if attempts < 3:
                        raise ValueError


                except ValueError:
                    print "Retrying...Retry number ", attempts+1
                    pass # retry
                else:
                    break # done


if __name__ == "__main__":

    # Check our lockfile and see if another copy is already running
    if daemonlock("s3-upload") != 0:
        sys.exit()
    # Connect to the bacula db and get our list of full volumes to
    # upload
    full_volumes = get_full_volumes()
    # Do the uploads to S3
    upload_volumes(full_volumes)