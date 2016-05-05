import logging

class LoggerHandlers:

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
        formatter = logging.Formatter(format_string)
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        logger.addHandler(fh)
        logger.addHandler(ch)
        return logger


# if __name__ == "__main__":
#     print 'testing code'
#     x= LoggerHandlers.login_to_file(LoggerHandlers(),'test',10,'/var/www/py/nc-backup-py/log/ncbackup.log')
#     x.critical('TEST')