import argparse
import time


from os import listdir
from os.path import isfile, join, isdir
from hashlib import md5
from Crypto.Cipher import AES
from Crypto import Random

from execution.subprocess_execution import SubprocessExecution
from cleanup.deletions import DeleteFiles


class EncryptionWorks:
    """OpenSSL encryption"""
    def encryption_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', type=str
                                   , help='Objectives to encrypt', required=True)
        parser_object.add_argument('-d', '--DESTINATION', type=str
                                   , help='Destination folder of the output', required=True)
        parser_object.add_argument('-k','--KEY_FILE', type=str
                                   , help='Compression key file', required=True)
        parser_object.add_argument('-s', '--FILE_SIZE', type=str
                                   , help='Output File size', required=False)
        parser_object.add_argument('-r', '--REMOVE_OBJECTIVES', type=str
                           , help='Remove/Delete objective folders', required=False)

        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def __derive_key_and_iv(self, password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def encrypt(self, in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = Random.new().read(bs - len('Salted__'))
        key, iv = self.__derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        out_file.write('Salted__' + salt)
        finished = False
        while not finished:
            chunk = in_file.read(1024 * bs)
            if len(chunk) == 0 or len(chunk) % bs != 0:
                padding_length = (bs - len(chunk) % bs) or bs
                chunk += padding_length * chr(padding_length)
                finished = True
            out_file.write(cipher.encrypt(chunk))

    def decrypt(self, in_file, out_file, password, key_length=32):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = self.__derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)

    def create_preconditions(self, destination):
        if not isdir(destination):
            execution_mkdir = SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + destination)
            SubprocessExecution.print_output(SubprocessExecution(), execution_mkdir)

if __name__ == "__main__":
    print "Encrypting files"
    encryption_command = EncryptionWorks.encryption_commands(EncryptionWorks())
    if encryption_command.OBJECTIVES and encryption_command.DESTINATION:
        EncryptionWorks.create_preconditions(EncryptionWorks(), encryption_command.DESTINATION)
        objectives_to_encrypt = encryption_command.OBJECTIVES.split(' ')
        datetime_string = time.strftime("%Y%m%d_%H%M%S")
        for objective in objectives_to_encrypt:
            only_files = [f for f in listdir(objective) if isfile(join(objective, f))]
            # print only_files
            for file_to_add in only_files:
                with open(objective + '/' + file_to_add, 'rb') as in_file, \
                        open(encryption_command.DESTINATION + '/' + datetime_string + '.tar.gz.crypt', 'wb') as out_file, \
                        open(encryption_command.KEY_FILE, 'r') as key_file:
                    key_from_file =key_file.read().replace('\n', '')
                    EncryptionWorks.encrypt(EncryptionWorks(), in_file, out_file,key_from_file)
                    # Compressed file is not a directory.

    if encryption_command.REMOVE_OBJECTIVES:
        print 'Deleting files after objective files as per config option --REMOVE_OBJECTIVES: ' \
              + encryption_command.OBJECTIVES
        DeleteFiles.remove_files(DeleteFiles(),encryption_command.OBJECTIVES)