import sys


class OSInformation:
    @staticmethod
    def isWindows():
        if getattr(sys, "getwindowsversion", None) is not None:
            return sys.getwindowsversion()[0] == 6
        else:
            return False


