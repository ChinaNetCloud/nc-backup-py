print "Encrypting files"
"""
cat "$KEY_FILE" "$FILE" | $GPGAGENT --daemon gpg2 --batch --yes --no-tty --quiet -c --passphrase-fd 0 | split  -d -b 4000m - "$FILE_GPG". #DL-NEW1#
"""