import os


class ConfigParser:
    def replace_end_backslash_and_spaces(self, dict_entire, logger=None):
        intro_message = 'PARSER: (pre-run script) checking backslashes and unnecesary spaces.'
        logger.info(intro_message)
        print intro_message

        for dict_section in dict_entire:
            if dict_section == 'GENERAL':
                parser_message = 'Checking GENERAL section'
                logger.info(parser_message)
                print parser_message
                # print dict_entire[dict_section]
                for section in dict_entire[dict_section]:
                    dict_entire[dict_section][section] = dict_entire[dict_section][section].lstrip()
                    dict_entire[dict_section][section] = dict_entire[dict_section][section].rstrip()
                    if os.path.exists(os.path.dirname(dict_entire[dict_section][section])):
                        # print dict_entire[dict_section][section]
                        logger.info(dict_entire[dict_section][section] + ' is interpreted as a path, parsing...')
                        dict_entire[dict_section][section] = self.parse_path(dict_entire[dict_section][section], logger)
            elif dict_entire[dict_section].get('PARAMETERS'):
                # print 'AAAA'
                for section in dict_entire[dict_section]:
                    if section == 'PARAMETERS':
                        # print section
                        for paramters_dict in dict_entire[dict_section]['PARAMETERS']:
                            pass
                            # print type(dict_entire[dict_section]['PARAMETERS'][paramters_dict])
                            # x = str(dict_entire[dict_section]['PARAMETERS'][paramters_dict])
                            # print type(x)
                            # if dict_entire[dict_section]['PARAMETERS'][paramters_dict] is not dict \
                            #         and dict_entire[dict_section]['PARAMETERS'][paramters_dict]:
                            #     dict_entire[dict_section]['PARAMETERS'][paramters_dict] = \
                            #         dict_entire[dict_section]['PARAMETERS'][paramters_dict].lstrip()
                            #     dict_entire[dict_section]['PARAMETERS'][paramters_dict] = \
                            #         dict_entire[dict_section]['PARAMETERS'][paramters_dict].rstrip()
                            #     print type(dict_entire[dict_section]['PARAMETERS'][paramters_dict])
                            #     if os.path.exists(os.path.dirname(dict_entire[dict_section]['PARAMETERS'][paramters_dict])) \
                            #             or os.path.exists(
                            #                 os.path.isfile(dict_entire[dict_section]['PARAMETERS'][paramters_dict])) \
                            #             or dict_entire[dict_section]['PARAMETERS'][paramters_dict][1:] == '/':
                            #         # print dict_entire[dict_section][section]
                            #         logger.info(
                            #             dict_entire[dict_section][section] + ' is interpreted as a path; parseing...')
                            #         dict_entire[dict_section][section] = \
                            #             self.parse_path(dict_entire[dict_section]['PARAMETERS'][paramters_dict], logger)

        return dict_entire

    def parse_path(self, path, logger=None):
        if path[-1] == '/':
            log_message = 'ending backslash from configs: ' + path
            logger.info(log_message)
            print log_message
            path = path[:-1]

        return path
