import argparse
import time
import sys
import random


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
        parser_object.add_argument('-o', '--OBJECTIVES', '--TARGETS', type=str
                                   , help='Objectives to encrypt', required=False)
        parser_object.add_argument('-D', '--DESTINATION', type=str
                                   , help='Destination folder of the output', required=False)
        parser_object.add_argument('-k','--KEY_FILE', type=str
                                   , help='Compression key file', required=False)
        parser_object.add_argument('-H','--HOME_FOLDER', type=str
                                   , help='Include the main forder to syspath so we '
                                          'can include other libraries', required=True)
        parser_object.add_argument('-s', '--FILE_SIZE', type=str
                                   , help='Output File size', required=False)
        parser_object.add_argument('-r', '--REMOVE_OBJECTIVES', '--REMOVE_TARGETS', type=str
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
        print password
        if python_version == '2.7':
            with open(password, 'r') as key_file:
                password = key_file.read().replace('\n', '')
            bs = AES.block_size

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
        elif python_version == '2.6':
            command_encrypt = 'cat ' + password + ' ' + in_file.name + \
                              ' | /usr/bin/gpg-agent --daemon gpg2  --cipher-algo AES-128 --batch --yes --no-tty ' \
                              '--quiet -c --passphrase-fd 0 > ' + out_file.name
            execution_encryption = SubprocessExecution.main_execution_function(SubprocessExecution(), command_encrypt, True)
            # print execution_encrytion
            if execution_encryption[0] == 0:
                return out_file.name

    def decrypt(self, in_file, out_file, password, key_length=32, home_folder=''):
        if python_version == '2.7':
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
        elif python_version == '2.6':
            command_decrypt = 'echo ' + password + ' ' \
                              '| gpg-agent --quiet  --daemon gpg2 --batch --yes -d --passphrase-fd 0 -o ' \
                              + out_file.name + ' ' \
                              + in_file.name
            execution_decryption = SubprocessExecution.main_execution_function(SubprocessExecution(), command_decrypt, True)
            if execution_decryption[0] == 0:
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

    @staticmethod
    def cat_files (path_to_file):
        command_cat = 'cat ' + path_to_file + '.* > ' + path_to_file
        print command_cat
        cat_execution = SubprocessExecution.main_execution_function(SubprocessExecution(), command_cat)
        return cat_execution

    def create_key_file(self,path_to_new_key_file,hash_size=None, python_version=None):
        print 'Creating a key file as the was not in the path'
        if python_version == '2.7':
            key_word = self.hash_key_generator_crypto(hash_size)
        elif python_version == '2.6':
            key_word = self.hash_key_generator_gpg(hash_size) + '\n'
        print key_word
        # exit(1)
        with open(path_to_new_key_file, 'a') as key_file:
            key_file.write(key_word)
            print 'New key file creation done'
            key_file.close()

    @staticmethod
    def hash_key_generator_gpg(chars=16):
        return ''.join(random.choice('0123456789abcdef') for i in range(chars))

    @staticmethod
    def hash_key_generator_crypto(bits=256):
        assert bits % 8 == 0
        # required_length = bits / 8 * 2
        s = hex(random.getrandbits(bits))
        print s
        s = s.lstrip('0x').rstrip('L')
        print s
        return s


if __name__ == "__main__":
    print "Encrypting/Decrypting files"
    # Object of encryption class
    encryption_command = EncryptionWorks.encryption_commands(EncryptionWorks())

    # Dynamic imporst using HOME_FOLDER as default value.
    sys.path.append(encryption_command.HOME_FOLDER)
    from execution.subprocess_execution import SubprocessExecution
    from tools.filesystem_handling import FilesystemHandling, remove_objectives
    from execution.config_parser import ConfigParser

    # Validate some Parameters and pass default values if absent
    if not ConfigParser.check_exists(ConfigParser(), encryption_command.OBJECTIVES) \
            and not ConfigParser.check_exists(ConfigParser(), encryption_command.DECRYPT):
        encryption_command.OBJECTIVES = '/opt/backup/compressed'
    if not ConfigParser.check_exists(ConfigParser(), encryption_command.DESTINATION) \
            and not ConfigParser.check_exists(ConfigParser(), encryption_command.DECRYPT):
        encryption_command.DESTINATION = '/opt/backup/encrypted'
    if not ConfigParser.check_exists(ConfigParser(), encryption_command.FILE_SIZE) \
            and not ConfigParser.check_exists(ConfigParser(), encryption_command.DECRYPT):
        encryption_command.FILE_SIZE = '4000'
    if not ConfigParser.check_exists(ConfigParser(), encryption_command.KEY_FILE) \
            and not ConfigParser.check_exists(ConfigParser(), encryption_command.DECRYPT):
        encryption_command.KEY_FILE = '/etc/nc-backup-py/key_file'
    if not ConfigParser.is_existing_abs_path(ConfigParser(), encryption_command.KEY_FILE):
        print "Creating Key files it does not exists"
        if python_version == '2.7':
            EncryptionWorks.create_key_file(EncryptionWorks(), encryption_command.KEY_FILE, 256, python_version)
        elif python_version == '2.6':
            EncryptionWorks.create_key_file(EncryptionWorks(), encryption_command.KEY_FILE, 16, python_version)
    if not ConfigParser.is_existing_abs_path(ConfigParser(),encryption_command.KEY_FILE):
        print 'You need a key file to encrypt: ' + str(encryption_command.KEY_FILE) \
              + ' Does not seem to exist. Stopping execution'
        exit(1)

    # Encryption
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
                        EncryptionWorks.split_binary_file(EncryptionWorks(), file_encrypted, encryption_command.FILE_SIZE)
                        FilesystemHandling.remove_files(out_file_str)

        remove_objectives(encryption_command.OBJECTIVES,
                          encryption_command.REMOVE_OBJECTIVES)

    # Decryption
    elif encryption_command.DECRYPT == '-d' or encryption_command.DECRYPT is True:
        print 'You have chosen to decrypt with -d option'
        if encryption_command.OBJECTIVES and encryption_command.DESTINATION:
            datetime_string = time.strftime("%Y%m%d_%H%M%S")
            if not encryption_command.OBJECTIVES.endswith('000'):
                cat_execution_result = EncryptionWorks.cat_files(encryption_command.OBJECTIVES)
                if cat_execution_result[0] != 0:
                    print 'Error:Cat retuned a non zero exit code.'
                    exit(1)
                with open(encryption_command.OBJECTIVES, 'rb') as in_file:
                    with open(encryption_command.DESTINATION, 'wb') as out_file:
                        with open(encryption_command.KEY_FILE, 'r') as key_file:
                            key_from_file = key_file.read().replace('\n', '')
                            EncryptionWorks.decrypt(EncryptionWorks(), in_file, out_file, key_from_file, 32,
                                                    encryption_command.HOME_FOLDER)
            else:
                result_name = encryption_command.OBJECTIVES.replace('.000', '')
                cat_execution_result = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                   'mv ' + encryption_command.OBJECTIVES + ' ' + result_name)

                with open(result_name, 'rb') as in_file:
                    with open(encryption_command.DESTINATION, 'wb') as out_file:
                        with open(encryption_command.KEY_FILE, 'r') as key_file:
                            key_from_file =key_file.read().replace('\n', '')
                            EncryptionWorks.decrypt(EncryptionWorks(), in_file, out_file, key_from_file, 32, encryption_command.HOME_FOLDER)
