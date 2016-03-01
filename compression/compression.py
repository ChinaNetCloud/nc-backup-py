import argparse
import time
import os


from execution.subprocess_execution import SubprocessExecution
from cleanup.deletions import DeleteFiles

class CompressionWorks:
    # def __init__(self):
    #     print 'Executing compression of files'

    def compression_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', type=str
                                   , help='Included fileset to compress', required=True)
        parser_object.add_argument('-d', '--DESTINATION', type=str
                                   , help='Compress files to folder', required=True)
        parser_object.add_argument('-r', '--REMOVE_OBJECTIVES', type=str
                                   , help='Remove/Delete objective folders', required=False)
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def compression_execution(self, objectives,destination):
        """Execute compression of files"""
        if objectives != '' and objectives is not None:
            objectives = objectives.replace(' /', ' ')
            objectives = objectives[1:]
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        tar_command = '/usr/bin/sudo /bin/tar czCf / ' + destination + '/filesbackup_' \
                          + datetime_string + '.tar.gz ' + objectives
        if not os.path.isdir(destination):
            execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + destination)
            SubprocessExecution.print_output(SubprocessExecution(), execution_mkdir)
        try:
            execution_message = SubprocessExecution.main_execution_function(SubprocessExecution(), tar_command)
            SubprocessExecution.print_output(SubprocessExecution(), execution_message)
        except Exception as e:
            e.args += (execution_message,)
            raise



if __name__ == "__main__":
    command_compression = CompressionWorks.compression_commands(CompressionWorks())
    if command_compression.OBJECTIVES and command_compression.DESTINATION:
        print 'Files to compress: ' + command_compression.OBJECTIVES + '. This files will be compressed to: '\
              + command_compression.DESTINATION
        tar_execution = CompressionWorks.compression_execution(CompressionWorks(), command_compression.OBJECTIVES
                                                               , command_compression.DESTINATION)
    if command_compression.REMOVE_OBJECTIVES:
        print 'Deleting files after objective files as per config option --REMOVE_OBJECTIVES: ' \
              + command_compression.OBJECTIVES
        DeleteFiles.remove_files(DeleteFiles(),command_compression.OBJECTIVES)

