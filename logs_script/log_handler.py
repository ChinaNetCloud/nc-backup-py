import logging
# import socket

# create logger
# module_logger = logging.getLogger('ncbackup.auxiliary')

class LoggerHandlers:
    # def __init__(self, a_hostname='localhost'):
    #     self.hostname = a_hostname
    #

    def rotating_logs(self):
        print 'to be DONE'

    def login_to_file(self,module_name='ncbackup', debug_level=10, log_file='log/ncbackup.log',
                 format_string = '%(asctime)s - %(hostname)s - %(name)s - %(levelname)s - %(message)s'):
        logger = logging.getLogger(module_name)
        logger.setLevel(debug_level)
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.ERROR)
        # logger.__setattr__('hostname','')
        formatter = logging.Formatter(format_string)
        # logging.Formatter()
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        # add the handlers to the logger
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger


if __name__ == "__main__":
    print 'testing code'
    x= LoggerHandlers.login_to_file(LoggerHandlers(),'test',10,'/var/www/py/nc-backup-py/log/ncbackup.log')
    x.critical('TEST')