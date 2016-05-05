import sys


class OSInformation:
    @staticmethod
    def isWindows():
        if getattr(sys, "getwindowsversion", None) is not None:
            return sys.getwindowsversion()[0] == 6
        else:
            return False
    @staticmethod
    def isLinux():
        if sys.platform == 'linux' or sys.platform == 'linux2':
            return sys.platform.linux_distribution
        else:
            return False



