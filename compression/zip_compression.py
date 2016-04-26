import os
import zipfile


class ZipCompression:
    def __init__(self, out_file, objective_files):
        zipf = zipfile.ZipFile(out_file, 'a', zipfile.ZIP_DEFLATED)
        self.__zipdir(objective_files, zipf)
        zipf.close()

    def __zipdir(self,objective_files, ziph):
        # ziph is zipfile handle
        for root, dirs, files in os.walk(objective_files):
            for file in files:
                ziph.write(os.path.join(root, file))


# x = ZipCompression('/opt/backup/local/test.zip','/home/abel/Documents')