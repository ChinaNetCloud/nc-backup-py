import argparse

class Storage:
    def storage_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', type=str
                                   , help='Objectives to encrypt', required=True)
        args_list, unknown = parser_object.parse_known_args()
        return args_list
    def list_content(self):
        print "Listing directory content"

    def upload_content(self):
        print 'Uploading to storage'

    def remove_content(self):
        print 'General: removing files from storage'

    def check_size_content(self):
        print 'checking the files size'


class StorageLocal (Storage):
    def list_content(self):
        print "Listing directory content"

    def upload_content(self):
        print 'Uploading to storage'

    def remove_content(self):
        print 'Local: removing files from storage'

    def check_size_content(self):
        print 'Localchecking the files size'


class AWSS3(Storage):
    def list_content(self):
        print "Listing directory content"

    def upload_content(self):
        print 'Uploading to storage'

    def remove_content(self):
        print 'S3: removing files from storage'

    def check_size_content(self):
        print 'checking the files size'


my_list = [Storage(), StorageLocal(), AWSS3()]



for x in my_list:
    x.remove_content()
