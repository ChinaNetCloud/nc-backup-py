"""Storage Execution Classes."""


class StorageExecution:

    def __init__(self):
        """Initalize and run."""
        import sys
        import os
        import json

        # print "os.getcwd(): %s" % os.getcwd()

        self.storage_cmd = self.get_args()

        sys.path.append(self.storage_cmd.HOME_FOLDER)

        # from pprint import pprint
        # pprint(self.storage_cmd)

        # Load storage_templates.json
        template_path = os.path.join(
            self.storage_cmd.HOME_FOLDER,
            self.storage_cmd.DEFAULT_TEMPLATE_FILE
        )
        with open(template_path, 'r') as f:
            self.templates = json.load(f)
        # pprint(self.templates)

        if self.storage_cmd.ACTION.lower() == "upload":
            self.upload_content()
        elif self.storage_cmd.ACTION.lower() == "remove":
            self.remove_content()
        elif self.storage_cmd.ACTION.lower() == "list":
            self.list_content()
        elif self.storage_cmd.ACTION.lower() == "size":
            self.check_size_content()
        else:
            print "ACTION %s is not defined." % self.storage_cmd.ACTION
            print "Available actions are UPLOAD, REMOVE, LIST, SIZE"
            exit(1)

    def get_args(self):
        """Get arguments to script."""
        import argparse
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument(
            '-o', '--OBJECTIVES', '--TARGETS',
            type=str,
            help='Objectives to encrypt',
            required=False
            )
        parser_object.add_argument(
            '-w', '--WORK_FOLDER',
            type=str,
            help='Backup working directory.',
            required=False
            )
        parser_object.add_argument(
            '-D', '--DESTINATION',
            type=str,
            help='Backup destination: local, s3, oss, etc',
            required=True)
        parser_object.add_argument(
            '-A', '--ACTION',
            type=str,
            help='Storage Action: upload, list or remove.',
            required=False,
            default='Upload')
        parser_object.add_argument(
            '-H', '--HOME_FOLDER',
            type=str,
            help='Path to the nc-backup-py folder',
            required=True)
        parser_object.add_argument(
            '-hn', '--HOSTNAME',
            type=str,
            help='Server name (client Host Name) e.g: nc-backup-kr',
            required=True)
        parser_object.add_argument(
            '-u', '--UPLOAD_COMMAND_TEMPLATE',
            type=str,
            help='Upload command template.',
            required=False)
        parser_object.add_argument(
            '-l', '--LS_COMMAND_TEMPLATE',
            type=str,
            help='List Command Template',
            required=False)
        parser_object.add_argument(
            '-r', '--RM_COMMAND_TEMPLATE',
            type=str,
            help='List Command Template',
            required=False)
        parser_object.add_argument(
            '-R', '--REMOVE_OBJECTIVES',
            '--REMOVE_TARGETS',
            type=str,
            help='Remove Encrypted files and folder after execution',
            required=False)
        parser_object.add_argument(
            '--ARGS_DICT',
            type=str,
            help='ARGS Dictionary',
            required=False,
            default="{}")
        parser_object.add_argument(
            '--DEFAULT_TEMPLATE_FILE',
            type=str,
            help='Default Templates File',
            required=False,
            default="storage/storage_templates.json")
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def iterate_result(self, uploads_to_cloud):
        succesful = 0
        count_file = 1
        print uploads_to_cloud
        for upload_to_cloud in uploads_to_cloud:
            if upload_to_cloud[0] is not 0:
                print 'upload of file number ' + str(
                    count_file) + ' failed to upload.'
                exit(1)
            count_file = count_file + 1

    def execute(self):
        print "calling %s command to upload." % self.storage_cmd.DESTINATION
        from storages import Storage
        command = Storage(self.storage_cmd)
        command_output = command.execute()
        if command_output:
            StorageExecution.iterate_result(StorageExecution(), command_output)
        else:
            print 'Executing %s retuned a None result' % self.storage_cmd.DESTINATION

    def list_content(self):
        """Set defaults for list if not present."""
        print "Listing directory content"

    def upload_content(self):
        """Set defaults for upload_command if not present."""
        if not self.storage_cmd.REMOVE_OBJECTIVES:
            self.storage_cmd.REMOVE_OBJECTIVES = 'True'
            print "WARNING: REMOVE_OBJECTIVES is missing, default is true."
        if not self.storage_cmd.OBJECTIVES:
            self.storage_cmd.OBJECTIVES = '/opt/backup/encrypted'
        print 'Storage Destination: ' + self.storage_cmd.DESTINATION

        if self.storage_cmd.UPLOAD_COMMAND_TEMPLATE:
            print "Using template %s " % self.storage_cmd.UPLOAD_COMMAND_TEMPLATE
        else:
            print "Trying to set default %s storage upload functions" % self.storage_cmd.DESTINATION
            if str(self.storage_cmd.DESTINATION) not in ['s3', 'oss', 'ssh', 'local']:
                print ('Upload command template for not available storage destination: %s ' % self.storage_cmd.DESTINATION)
                print 'You can use your own template for the upload command. See:'
                print '<add link to docs>'
                exit(1)
            else:
                self.storage_cmd.UPLOAD_COMMAND_TEMPLATE = self.templates[self.storage_cmd.DESTINATION]['UPLOAD_COMMAND_TEMPLATE']
                print "Sucessfully set Upload command template for %s." % self.storage_cmd.DESTINATION

    def remove_content(self):
        """Set defaults for remove if not present."""
        print 'General: removing files from storage'

    def check_size_content(self):
        """Set defaults for size if not present."""
        print 'checking the files size'


if __name__ == "__main__":

    executor = StorageExecution()
    executor.execute()
