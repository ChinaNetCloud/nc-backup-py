import sys
import os


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

    def find_mount_point_linux(self, path):
        path = os.path.abspath(path)
        while not os.path.ismount(path):
            path = os.path.dirname(path)
        return path
    def get_disk_usage(self, path):
        disk = os.statvfs(path)
        capacity = disk.f_bsize * disk.f_blocks
        used = disk.f_bsize * (disk.f_blocks - disk.f_bavail)
        available = disk.f_bsize * disk.f_bavail
        return capacity, used, available

    @staticmethod
    def human_readable_size(nbytes):
        suffixes = ['B', 'KB', 'MB', 'GB', 'TB', 'PB']
        if nbytes == 0: return '0 B'
        i = 0
        while nbytes >= 1024 and i < len(suffixes) - 1:
            nbytes /= 1024.
            i += 1
        f = ('%.2f' % nbytes).rstrip('0').rstrip('.')
        return '%s %s' % (f, suffixes[i])


