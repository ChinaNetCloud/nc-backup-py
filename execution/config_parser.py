import os


class ConfigParser:
    def validator_basic(self, dict_entire, logger=None):
        intro_message = 'PARSER: (pre-run script) doing basic config validations.'
        logger.info(intro_message)
        print intro_message

        for dict_section in dict_entire:
            if dict_section == 'GENERAL':
                parser_message = 'GENERAL'
                logger.info(parser_message)
                print parser_message
                for section in dict_entire[dict_section]:
                    dict_entire[dict_section][section] = \
                        self.remove_pesiding_and_ending_characters(dict_entire[dict_section][section], logger)
                    if self.is_abs_path(dict_entire[dict_section][section]):
                        logger.info(dict_entire[dict_section][section] + ' is interpreted as a path, parsing...')
                        dict_entire[dict_section][section] = \
                            self.remove_backslash_from_path(dict_entire[dict_section][section], logger)
            # Validating common parameters
            elif dict_entire[dict_section].get('PARAMETERS'):
                print dict_section
                logger.info(dict_section)
                #Filesets exclude
                if dict_entire[dict_section]['PARAMETERS'].get('FILESET_INCLUDE'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'FILESET_INCLUDE', logger)
                if dict_entire[dict_section]['PARAMETERS'].get('FILESET_EXCLUDE'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'FILESET_EXCLUDE', logger)
                # Destination validation
                if dict_entire[dict_section]['PARAMETERS'].get('DESTINATION'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'DESTINATION', logger)
                # Objectives Validation
                if dict_entire[dict_section]['PARAMETERS'].get('OBJECTIVES'):
                    dict_entire = self.validation_path_parameters(dict_entire,dict_section,'OBJECTIVES',logger)
                #MySQL
                if dict_entire[dict_section]['PARAMETERS'].get('CREDENTIAL_PATH'):
                    dict_entire = self.validation_path_parameters(dict_entire,dict_section,'CREDENTIAL_PATH',logger)
                if dict_entire[dict_section]['PARAMETERS'].get('CONF_PATH'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'CONF_PATH', logger)
                if dict_entire[dict_section]['PARAMETERS'].get('DATA_DIR'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'DATA_DIR', logger)
                if dict_entire[dict_section]['PARAMETERS'].get('BINLOG_PATH'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'BINLOG_PATH', logger)
                if dict_entire[dict_section]['PARAMETERS'].get('MYSQL_DUMP_BINARY'):
                    dict_entire = self.validation_path_parameters(
                        dict_entire, dict_section, 'MYSQL_DUMP_BINARY', logger)
                if dict_entire[dict_section]['PARAMETERS'].get('MYSQL_BINARY'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'MYSQL_BINARY', logger)
                #Encryption
                if dict_entire[dict_section]['PARAMETERS'].get('KEY_FILE'):
                    dict_entire = self.validation_path_parameters(dict_entire, dict_section, 'KEY_FILE', logger)
        return dict_entire

    def validation_path_parameters(self,dict_entire, dict_section, path_name, logger=None, compulsory=False):
        print_path_name = ' |_' + path_name
        print print_path_name
        logger.info(print_path_name)
        if dict_entire[dict_section]['PARAMETERS'][path_name]:
            dict_entire[dict_section]['PARAMETERS'][path_name] = \
                self.remove_pesiding_and_ending_characters(
                    dict_entire[dict_section]['PARAMETERS'][path_name], logger)
            array_objectives = dict_entire[dict_section]['PARAMETERS'][path_name].split()
            for key, objective_string in enumerate(array_objectives):
                array_objectives[key] = \
                    self.remove_pesiding_and_ending_characters(array_objectives[key], logger)
                array_objectives[key] = self.remove_backslash_from_path(array_objectives[key], logger)
            dict_entire[dict_section]['PARAMETERS'][path_name] = ''
            if len(array_objectives) > 1:
                for key, objective_string in enumerate(array_objectives):
                    if key < len(array_objectives):
                        dict_entire[dict_section]['PARAMETERS'][path_name] += array_objectives[key] + ' '
                    else:
                        dict_entire[dict_section]['PARAMETERS'][path_name] += array_objectives[key]
            else:
                dict_entire[dict_section]['PARAMETERS'][path_name] = array_objectives[0]

            if dict_entire[dict_section]['PARAMETERS'][path_name][1:] == ' ' \
                    or dict_entire[dict_section]['PARAMETERS'][path_name][:-1] == ' ':
                dict_entire[dict_section]['PARAMETERS'][path_name] = \
                    self.remove_pesiding_and_ending_characters(
                        dict_entire[dict_section]['PARAMETERS'][path_name], logger)
        return dict_entire
    def validate_not_empty(self, text_string=None):
        if not text_string or text_string == '':
            return False
        else:
            return True

    #Validation of Destination and Objectives.
    def validate_destination(self, destination):
        # print destination
        if not self.validate_not_empty(destination):
            # print 'Empty'
            return False
        elif destination == 's3' or str(destination) == 'oss' or \
            str(destination) == 'local' or str(destination) == 'ssh':
            return True
        elif not self.is_abs_path(destination):
            return False
        return True

    def is_abs_path(self, path_to_check):
        return os.path.isabs(path_to_check)

    def is_existing_abs_path(self, path_to_check):
        if self.is_abs_path(path_to_check) and (os.path.isfile(path_to_check) or os.path.isdir(path_to_check)):
            return True
        return False

    def remove_pesiding_and_ending_characters(self, text_string, logger=None):
        before = text_string
        text_string = text_string.lstrip()
        text_string = text_string.rstrip()
        if before != text_string:
            log_message = 'Removed unnecessary white spaces at the begining and the end of ' + text_string
            logger.info(log_message)
            print log_message
        return text_string

    def remove_backslash_from_path(self, path, logger=None):
        if path[-1] == '/':
            log_message = 'Ending backslash from configs ' + path + \
                          ' it will be removed for execution to be: ' + path[:-1]
            logger.info(log_message)
            print log_message
            path = path[:-1]
        return path