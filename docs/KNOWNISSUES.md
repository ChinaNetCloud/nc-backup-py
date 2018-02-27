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
