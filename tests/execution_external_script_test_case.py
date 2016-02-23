import unittest

from collections import OrderedDict
from execution.backup_execution import BackupExecutionLogic

class ExecuteExternalScriptTestCase (unittest.TestCase):
    def test_invalid_path_given_in_config(self):
        # dict_test = OrderedDict([(u'fileset', OrderedDict([(u'action', u'execute'), (u'name', u'filesbackup'),
        #                                                    (u'FILESET_INCLUDE', [u'/etc', u'/var/www/py/nc-backup-py']),
        #                                                    (u'FILESET_EXCLUDE', [u'']),
        #                                                    (u'PATH', u''),
        #                                                    (u'EXECUTABLE', u''),
        #                                                    (u'PARAMETERS', u'')]))])
        #
        # path_test = dict_test['general']['HOME_FOLDER'] + '/' + dict_test['fileset']['name'] + '/' + dict_test['fileset']['name'] + '.py'
        # # print path_test
        # print BackupExecutionLogic.__execute_external_script(BackupExecutionLogic(),
        #                                                             dict_test,
        #                                                             dict_test['general']['HOME_FOLDER'])
        # self.assertNotEqual(BackupExecutionLogic.iterate_config_script(BackupExecutionLogic(),
        #                                                             dict_test,
        #                                                             dict_test['general']['HOME_FOLDER']),
        #                  path_test,
        #                  'File not found at ' + path_test)
        # self.ass
