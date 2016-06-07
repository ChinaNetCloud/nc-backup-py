import argparse
import time
import sys


from os import listdir
from os.path import isfile, join, isdir


python_version = '2.7'
if sys.version_info[0] == 2 and sys.version_info[1] == 7:
    python_version = '2.7'
    from Crypto import Random
    from hashlib import md5
    from Crypto.Cipher import AES
elif sys.version_info[0] == 2 and sys.version_info[1] < 7 and sys.version_info[1] > 5:
    python_version = '2.6'
else:
    print 'Unsupported python version, you are on your own'
    python_version = 'Unsupported'

class EncryptionWorks:
    """OpenSSL encryption"""
    def encryption_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-o', '--OBJECTIVES', type=str
                                   , help='Objectives to encrypt', required=True)
        parser_object.add_argument('-D', '--DESTINATION', type=str
                                   , help='Destination folder of the output', required=True)
        parser_object.add_argument('-k','--KEY_FILE', type=str
                                   , help='Compression key file', required=True)
        parser_object.add_argument('-H','--HOME_FOLDER', type=str
                                   , help='Include the main forder to syspath so we '
                                          'can include other libraries', required=True)
        parser_object.add_argument('-s', '--FILE_SIZE', type=str
                                   , help='Output File size', required=False)
        parser_object.add_argument('-r', '--REMOVE_OBJECTIVES', type=str
                           , help='Remove/Delete objective folders', required=False)
        parser_object.add_argument('-d', '--DECRYPT', help='Decrypt file', action="store_true")
        args_list, unknown = parser_object.parse_known_args()
        return args_list

    def __derive_key_and_iv(self, password, salt, key_length, iv_length):
        d = d_i = ''
        while len(d) < key_length + iv_length:
            d_i = md5(d_i + password + salt).digest()
            d += d_i
        return d[:key_length], d[key_length:key_length+iv_length]

    def encrypt(self, in_file, out_file, password, key_length=32, python_version='2.7', home_folder=''):
        # print python_version
        if python_version == '2.7':
            bs = AES.block_size
            with open(password, 'r') as key_file:
                password = key_file.read().replace('\n', '')
            salt = Random.new().read(bs - len('Salted__'))
            key, iv = self.__derive_key_and_iv(password, salt, key_length, bs)
            cipher = AES.new(key, AES.MODE_CBC, iv)
            out_file.write('Salted__' + salt)
            finished = False
            while not finished:
                chunk = in_file.read(1024 * bs)
                if len(chunk) == 0 or len(chunk) % bs != 0:
                    padding_length = bs - (len(chunk) % bs)
                    chunk += padding_length * chr(padding_length)
                    finished = True
                out_file.write(cipher.encrypt(chunk))
        else:
            # (echo 08df2cecc643985e7c274de03a819b21;
            # cat / opt / test / compressed / filesbackup_20160526_212715.tar.gz) | / usr / bin / gpg - agent - -daemon
            # gpg2 - -batch - -yes - -no - tty - -quiet - c - -passphrase - fd
            # 0 > / opt / test / encrypted / 20160526
            # _212844.tar.gz.crypt
            command_encrypt = 'cat '+ password +' '+ in_file.name +\
                              ' | /usr/bin/gpg-agent --daemon gpg2 --batch --yes --no-tty ' \
                              '--quiet -c --passphrase-fd 0 > ' + out_file.name
            execution_encrytion = SubprocessExecution.main_execution_function(SubprocessExecution(), command_encrypt, True)
            print execution_encrytion

            if execution_encrytion[0] == 0:
                return out_file.name


    def decrypt(self, in_file, out_file, password, key_length=32, home_folder=''):
        bs = AES.block_size
        salt = in_file.read(bs)[len('Salted__'):]
        key, iv = self.__derive_key_and_iv(password, salt, key_length, bs)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        next_chunk = ''
        finished = False
        print out_file
        # print in_file
        while not finished:
            chunk, next_chunk = next_chunk, cipher.decrypt(in_file.read(1024 * bs))
            if len(next_chunk) == 0:
                padding_length = ord(chunk[-1])
                if padding_length < 1 or padding_length > bs:
                   raise ValueError("bad decrypt pad (%d)" % padding_length)
                # all the pad-bytes must be the same
                if chunk[-padding_length:] != (padding_length * chr(padding_length)):
                   # this is similar to the bad decrypt:evp_enc.c from openssl program
                   raise ValueError("bad decrypt")
                chunk = chunk[:-padding_length]
                finished = True
            out_file.write(chunk)
        return out_file.name

    def split_file(self,path_to_file, chunk_size):
        # To be deprecated in favor of split_binary_file
        print path_to_file
        command_split = 'split --bytes=' + chunk_size + 'M ' + path_to_file + ' ' + path_to_file
        print command_split
        execution_split = SubprocessExecution.main_execution_function(SubprocessExecution(), command_split, True)
        # SubprocessExecution.print_output(SubprocessExecution(), execution_split)

    def split_binary_file(self, path_to_file, chunk_size):
        chunk_size =  int(chunk_size) * 1024 * 1024  # 500Mb  - max chapter size
        BUF = 50 * 1024 * 1024  # 50GB   - memory buffer size
        chapters = 0
        uglybuf = ''
        with open(path_to_file, 'rb') as src:
            while True:
                tgt = open(path_to_file + '.%03d' % chapters, 'wb')
                written = 0
                while written < chunk_size:
                    tgt.write(uglybuf)
                    tgt.write(src.read(min(BUF, chunk_size - written)))
                    written += min(BUF, chunk_size - written)
                    uglybuf = src.read(1)
                    if len(uglybuf) == 0:
                        break
                tgt.close()
                if len(uglybuf) == 0:
                    break
                chapters += 1

    def cat_files (self,path_to_file):
        command_cat = 'cat ' + path_to_file + '* > ' + path_to_file
        print command_cat
        cat_execution = SubprocessExecution.main_execution_function(SubprocessExecution(), command_cat)
        # SubprocessExecution.print_output(SubprocessExecution(), cat_execution)
        return cat_execution

if __name__ == "__main__":
    print "Encrypting/Decrypting files"
    encryption_command = EncryptionWorks.encryption_commands(EncryptionWorks())
    sys.path.append(encryption_command.HOME_FOLDER)
    from execution.subprocess_execution import SubprocessExecution
    from tools.filesystem_handling import FilesystemHandling
    from execution.config_parser import ConfigParser
    if not ConfigParser.is_existing_abs_path(ConfigParser(),encryption_command.KEY_FILE):
        print 'You need a key file to encrypt: ' + str(encryption_command.KEY_FILE) \
              + 'Does not seem to exist. Stopping execution'
        exit(1)
    if encryption_command.DECRYPT is None \
            or encryption_command.DECRYPT == '-e' \
            or encryption_command.DECRYPT == False:
        if not isfile(encryption_command.KEY_FILE):
            print 'The encription key file was NOT found at: ' + encryption_command.KEY_FILE
            exit(1)
        print encryption_command.OBJECTIVES

        if not ConfigParser.is_existing_abs_path(ConfigParser(), encryption_command.OBJECTIVES) \
                or not ConfigParser.is_abs_path(ConfigParser(), encryption_command.DESTINATION):
            print 'Please make sure OBJECTIVES exist and DESTINATION is absolute path, execution will not continue'
            exit(1)
        if encryption_command.OBJECTIVES and encryption_command.DESTINATION:
            FilesystemHandling.create_directory(encryption_command.DESTINATION)
            objectives_to_encrypt = encryption_command.OBJECTIVES.split(' ')
            datetime_string = time.strftime("%Y%m%d_%H%M%S")
            for objective in objectives_to_encrypt:
                only_files = [f for f in listdir(objective) if isfile(join(objective, f))]
                print only_files
                print objective
                # exit(0)
                for file_to_add in only_files:
                    out_file_str = encryption_command.DESTINATION + '/' + datetime_string + '.tar.gz.crypt'
                    with open(objective + '/' + file_to_add, 'rb') as in_file:
                        with open(out_file_str, 'wb') as out_file:
                            file_encrypted = EncryptionWorks.encrypt(EncryptionWorks(), in_file, out_file,
                                                    encryption_command.KEY_FILE, 32,
                                                    python_version, encryption_command.HOME_FOLDER)
                    # Split only if requested
                    if encryption_command.FILE_SIZE is not None and \
                                    int(encryption_command.FILE_SIZE) >= 1 and python_version == '2.7':
                        EncryptionWorks.split_binary_file(EncryptionWorks(),out_file_str,encryption_command.FILE_SIZE)
                        FilesystemHandling.remove_files(out_file_str)
                    elif encryption_command.FILE_SIZE is not None and \
                                    int(encryption_command.FILE_SIZE) >= 1 and python_version == '2.6':
                        EncryptionWorks.split_file(EncryptionWorks(), file_encrypted, encryption_command.FILE_SIZE)
                        FilesystemHandling.remove_files(out_file_str)

        # Compressed file is not a directory.
        if encryption_command.REMOVE_OBJECTIVES == 'True' or  encryption_command.REMOVE_OBJECTIVES == True:
            print 'Deleting files after objective files as per config option --REMOVE_OBJECTIVES: ' \
                  + encryption_command.OBJECTIVES
            FilesystemHandling.remove_files(encryption_command.OBJECTIVES)

    elif encryption_command.DECRYPT == '-d' or encryption_command.DECRYPT is True:
        if encryption_command.OBJECTIVES and encryption_command.DESTINATION:
            datetime_string = time.strftime("%Y%m%d_%H%M%S")
            if not encryption_command.OBJECTIVES.endswith('000'):
                cat_execution_result = EncryptionWorks.cat_files(EncryptionWorks(), encryption_command.OBJECTIVES)
                with open(encryption_command.OBJECTIVES, 'rb') as in_file:
                    with open(cat_execution_result, 'wb') as out_file:
                        with open(encryption_command.KEY_FILE, 'r') as key_file:
                            key_from_file = key_file.read().replace('\n', '')
                            EncryptionWorks.decrypt(EncryptionWorks(), in_file, out_file, key_from_file, 32,
                                                    encryption_command.HOME_FOLDER)
                        # Compressed file is not a directory.
            else:
                result_name = encryption_command.OBJECTIVES.replace('.000', '')
                cat_execution_result = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                   'mv ' + encryption_command.OBJECTIVES + ' ' + result_name)

                with open(result_name, 'rb') as in_file:
                    with open(encryption_command.DESTINATION, 'wb') as out_file:
                        with open(encryption_command.KEY_FILE, 'r') as key_file:
                            key_from_file =key_file.read().replace('\n', '')
                            EncryptionWorks.decrypt(EncryptionWorks(), in_file, out_file, key_from_file, 32, encryption_command.HOME_FOLDER)
                            # Compressed file is not a directory.

