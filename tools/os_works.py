import sys


class OSInformation:
    def isVista():
        if getattr(sys, "getwindowsversion", None) is not None:
            return sys.getwindowsversion()[0] == 6
        else:
            return False