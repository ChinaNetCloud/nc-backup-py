# Known issues

## ssl issues on python 2.6

You get the following warning:

`/usr/lib/python2.6/site-packages/pip/_vendor/requests/packages/urllib3/util/ssl_.py:90: InsecurePlatformWarning: A true SSLContext object is not available. This prevents urllib3 from configuring SSL appropriately and may cause certain SSL connections to fail. For more information, see https://urllib3.readthedocs.org/en/latest/security.html#insecureplatformwarning.
 InsecurePlatformWarning`

Please ignore this message; the software works just fine, this is a problem with a deprecated ssl python library.

## gpg-agent --daemon on python 2.6

If you see this error below:

```bash
can not connect to /home/user/.gnupg/S.gpg-agent: No such file or directory
```

Then launch gpg agent daemon:

```bash
$ gpg-agent --daemon
GPG_AGENT_INFO=/tmp/gpg-Y1AjlZ/S.gpg-agent:2523:1; export GPG_AGENT_INFO;
then you’ll just have to create a symbolic link:
$ cp -fs /tmp/gpg-Y1AjlZ/S.gpg-agent ~/.gnupg/
```

## AWS CLI integration

Q: Does the AWS CLI validate checksums?
The AWS CLI will perform checksum validation for uploading and downloading files in specific scenarios. Upload The AWS CLI will calculate and auto-populate the Content-MD5 header for both standard and multipart uploads. If the checksum that S3 calculates does not match the Content-MD5 provided, S3 will not store the object and instead will return an error message back the AWS CLI. The AWS CLI will retry this error up to 5 times before giving up. On the case that any files fail to transfer successfully to S3, the AWS CLI will exit with a non zero RC. See aws help returncodes for more information. Taken from AWS CLI FAQ
