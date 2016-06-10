import os
import string


from tools.sample_module import ModuleFrame
from execution.subprocess_execution import SubprocessExecution


class PostgresBackup(ModuleFrame):
    def __init__(self, parameters=None, logger=None):
        self.__parameters_dict = parameters
        self.__logger = logger

    def works_execution(self):
        if self.__parameters_dict['DESTINATION'] and self.__parameters_dict['PREFIX_FOLDER']:
            save_dir = self.__parameters_dict['DESTINATION'] \
                       + '/' + self.__parameters_dict['PREFIX_FOLDER'] + '/'
            if not os.path.isdir(save_dir):
                SubprocessExecution.main_execution_function(SubprocessExecution(), 'mkdir ' + save_dir,
                                                        self.__logger)
            if self.__parameters_dict['EXCLUDE_DB'] is not None or self.__parameters_dict['EXCLUDE_DB'] == '':
                exclude_db = self.__parameters_dict['EXCLUDE_DB'].split()
                exclude_db.append('template0')
                exclude_db.append('template1')
                exclude_db.append('|')
            else:
                exclude_db =['template0', 'template1', '|']
            # 'psql -l' produces a list of PostgreSQL databases.
            get_list = os.popen('psql -l').readlines()
            # Exclude header and footer lines.
            db_list = get_list[3:-2]
            # Extract database names from first element of each row.
            for n in db_list:
                n_row = string.split(n)
                n_db = n_row[0]
                # Pipe database dump through gzip
                # into .gz files for all databases
                # except template*.
                if n_db in exclude_db:
                    pass
                else:
                    print n_db
                    os.popen('pg_dump ' + n_db + ' | gzip -c > ' + save_dir + n_db + '.gz')

