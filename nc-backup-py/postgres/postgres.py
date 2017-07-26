import os
import string


from tools.sample_module import ModuleFrame
from execution.subprocess_execution import SubprocessExecution


class PostgresBackup(ModuleFrame):
    def __init__(self, parameters=None, logger=None):
        self.__parameters_dict = parameters
        self.__logger = logger

    def works_execution(self):
        self.__execution_result = True
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
            # get_list = os.popen('psql -l').readlines()
            get_list = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                   'psql -l', True, self.__logger)
            if get_list[0] == 0:
                get_list = get_list[1].split('\n')
            else:
                self.__execution_result = False
                self.__logger.critical('Error code: ' + str(get_list[0]))
                self.__logger.critical('StdOut: ' + get_list[1])
                self.__logger.critical('StdErr: ' + get_list[2])
                # print get_list[2]
                return 'Execution faile due to error listing postgres DBs'
            # Exclude header and footer lines.
            db_list = get_list[3:-3]

            # print db_list
            # Extract database names from first element of each row.
            for n in db_list:
                n_row = string.split(n)
                # print n_row
                n_db = n_row[0]
                # Pipe database dump through gzip
                # into .gz files for all databases
                # except template*.
                if n_db in exclude_db:
                    pass
                else:
                    print n_db
                    result_dump = \
                        SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                    'pg_dump ' + n_db + ' | gzip -c > ' + save_dir + n_db + '.gz'
                                                                    , True, self.__logger)
                    if result_dump[0] != 0:
                        self.__execution_result = False
                        self.__logger.critical('Error code: ' + str(result_dump[0]))
                        self.__logger.critical('StdOut: ' + result_dump[1])
                        self.__logger.critical('StdErr: ' + result_dump[2])
                        return 'Execution failed while executing: ' + 'pg_dump ' + n_db + ' | gzip -c > ' + save_dir + n_db + '.gz'
            # if DB backup ROLES.
            # https://www.postgresql.org/docs/8.1/static/app-pg-dumpall.html
            # option: --globals-only
            # this is before 8.3
            # on 8.3 they added --roles-only
            # https://www.postgresql.org/docs/8.3/static/app-pg-dumpall.html
            # but still have --globals-only
            # Need to add condition for older versions of postgress.
            result_dump = \
                SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                        'pg_dumpall -r | gzip -c > ' + save_dir + 'roles' + '.gz'
                                                        , True, self.__logger)
            print result_dump
        else:
            self.__execution_result = False
    # def __log_critical_error(self):

    def output(self):
        if self.__execution_result is True:
            return 0, 'Success', ''
        else:
            return 1, '', 'Error'

