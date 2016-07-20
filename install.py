import os
# from

if os.geteuid() != 0:
    print "Error: This installer needs to be executed by root"
    exit(1)


