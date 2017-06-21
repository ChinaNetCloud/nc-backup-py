import argparse

class backupCommands:
    def feature_commands(self):
        parser_object = argparse.ArgumentParser()
        group_run = parser_object.add_mutually_exclusive_group()
        group_run.add_argument('-r', '--run', help='Run script',
                                   action="store_true")
        group_run.add_argument('-t', '--test', help='Test run script',
                                   action="store_true")
        parser_object.add_argument('-c', '--config', type=str, help='Configuration file path', required=True)
        parser_object.add_argument('-l', '--logging_level', type=str,
                                   help='Loggin levels: INFO, WARNING, DEBBUG, default value is WARNING',
                                   required=False)

        args_list = parser_object.parse_args()
        return args_list