import time


from os import path


from subprocess_execution import SubprocessExecution
from tools.os_works import OSInformation


class BackupExecutionLogic:
    """Scripts execution logic"""
    def iterate_config_script(self,json_dict, home, logger=None):
        c = 1
        result = []
        start_time = time.time()
        for scripts_modules in json_dict:
            log_sring = "Section " + str(c) + ": " + scripts_modules + '.'
            print log_sring
            logger.info(log_sring)
            start_time = time.time()
            result_message = []
            if scripts_modules != 'GENERAL':

                # Check disk space OSInformation
                if not json_dict['GENERAL'].get('DISK_SPACE_CHECK') or \
                                json_dict['GENERAL']['DISK_SPACE_CHECK'] != 'False':
                    mounting_point = OSInformation.find_mount_point_linux(OSInformation(),
                                                                          json_dict['GENERAL']['WORK_FOLDER'])
                    if not json_dict['GENERAL'].get('DISK_SPACE_THRESHOLD'):
                        json_dict['GENERAL']['DISK_SPACE_THRESHOLD'] = 20
                    else:
                        json_dict['GENERAL']['DISK_SPACE_THRESHOLD'] = float(json_dict['GENERAL']['DISK_SPACE_THRESHOLD'])
                    space_before_execution = OSInformation.get_disk_usage(OSInformation(), mounting_point)
                    average_calculation = 100 * space_before_execution[2] / space_before_execution[0]
                    space_string_before_execution = 'Parition size: {0}, Used: {1}, Avail: {2}, this is {3}% available'\
                        .format(
                        str(OSInformation.human_readable_size(space_before_execution[0])),
                        str(OSInformation.human_readable_size(space_before_execution[1])),
                        str(OSInformation.human_readable_size(space_before_execution[2])),
                        str(average_calculation))
                    print space_string_before_execution
                    if json_dict['GENERAL']['DISK_SPACE_THRESHOLD'] > \
                            average_calculation >= json_dict['GENERAL']['DISK_SPACE_THRESHOLD']/2:
                        logger.warning(space_string_before_execution)
                    elif json_dict['GENERAL']['DISK_SPACE_THRESHOLD']/2 > average_calculation <= json_dict['GENERAL']['DISK_SPACE_THRESHOLD']/6:
                        logger.critical(space_string_before_execution)
                    elif average_calculation <= json_dict['GENERAL']['DISK_SPACE_THRESHOLD']/10 and space_before_execution[2] >100:
                        logger.critical('Less than one percent space available, Stopping execution')
                        result_message.append({'external':
                                                   {'message':
                                                        (1, space_string_before_execution, 'stderr: No space left')
                                                    }
                                               })
                        return result_message
                    elif space_before_execution[2] < 100:
                        result_message.append({'external':
                                                   {'message':
                                                        (1, space_string_before_execution, 'stderr: No space left')
                                                    }
                                               })
                        return result_message
                    else:
                        logger.info(space_string_before_execution)
                for section in json_dict[scripts_modules]:
                    external_execution = self.__execute_selection_of_external_script(section,json_dict,scripts_modules,
                                                                                     home, logger)
                    if external_execution:
                        result_message.append(external_execution)
            c += 1
            if result_message:
                result.append(result_message)
            time_log_final = 'Execution time in seconds: ' + str(time.time() - start_time)
            print time_log_final
            logger.info(time_log_final)
        return result

    def __execute_selection_of_external_script(self,section ,json_dict, scripts_modules, home_folder, logger=None):
        loaded_scripts = []
        # Load independent executable
        if section == 'ACTION' and json_dict[scripts_modules][section] == "execute":
            log_string = "Loading executable module: " + json_dict[scripts_modules]['NAME']
            print log_string
            logger.info(log_string)
            module_to_call = self.__prepare_configs_for_execution(json_dict,scripts_modules,home_folder, logger)
            logger.info('Prapare execution finised script. Now prepare parameters to pass is going to be executed')
            pass_parameters = self.__organize_parameters_for_custom_script(json_dict[scripts_modules],
                                                                           json_dict['GENERAL'], logger)
            logger.info('Finished parameters preparation for section')

            if path.isfile(module_to_call):
                log_string = "Loading from file: " + module_to_call
                print log_string
                logger.info(log_string)
            if pass_parameters is not None:
                module_to_call = module_to_call + ' ' + pass_parameters
                module_call_message = 'Calling module: ' + module_to_call
                print module_call_message
                logger.info(module_call_message)

            out_put_exec = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                            module_to_call, True, logger)

            if out_put_exec[0] is not 0:
                logger.critical('Error executing external script')
                logger.critical('Eddor Code: ' + str(out_put_exec[0]) + \
                                ' StdOut: ' + out_put_exec[1] + \
                                ' StdErr: ' + str(out_put_exec[2]))
            elif out_put_exec[0] is 0:
                logger.info('the execution was succesfull')
                logger.info('StdOut: ' + out_put_exec[1])
            loaded_scripts = {'external':{'message': out_put_exec}}
            return loaded_scripts

        # Load plugins dynamically
        elif section == 'ACTION' and json_dict[scripts_modules][section] == "load":
            path_to_import = json_dict[scripts_modules]['FROM'] + '.' + json_dict[scripts_modules]['FILENAME']
            loading_plugin = 'Loadable dependant module (plugin): ' + path_to_import
            print loading_plugin
            logger.info(loading_plugin)
            plugin_object = DynamicImporter(path_to_import, json_dict[scripts_modules]['CLASS'], )
            if json_dict[scripts_modules].get('PARAMETERS'):
                instanciated_plugin = plugin_object.create_object(json_dict[scripts_modules]['PARAMETERS'], logger)
            else:
                instanciated_plugin = plugin_object.create_object(logger)

            instanciated_plugin.config_plugin()
            works_execution = instanciated_plugin.works_execution()
            logger.info('Plugin works_execution function output: ' + str(works_execution))
            output = instanciated_plugin.output()
            print output
            if json_dict[scripts_modules]['FILENAME'] == 'size_calculation':
                logger.info('Output: ' + str(output))
                loaded_scripts = {'plugin':{'size': output}}
                return loaded_scripts
            else:
                return {'plugin': {'message': output}}

    def __prepare_configs_for_execution(self, json_dict,scripts_modules,home_folder, logger=None):
        """Prepare configurations for execution create path, get parameters, etc"""
        call_module = ''
        if json_dict[scripts_modules].get('EXECUTE_WITH') == None \
                or json_dict[scripts_modules].get('EXECUTE_WITH') == '':
            call_module = 'python '
            logger.info('Automatically selected python as execution method')
        else:
            call_module = json_dict[scripts_modules]['EXECUTE_WITH'] + ' '
            logger.info('Config asked to execute module with: ' + call_module)

        call_module += home_folder + '/'
        # print call_module
        if json_dict[scripts_modules].get('EXECUTABLE') == None \
                or json_dict[scripts_modules].get('EXECUTABLE') == '':
            json_dict[scripts_modules]['EXECUTABLE'] = json_dict[scripts_modules]['NAME'] + '.py'
        call_module += json_dict[scripts_modules]['NAME'] + '/' + json_dict[scripts_modules]['EXECUTABLE']
        logger.info('Preraring for execution as follows: ' + call_module)
        return call_module

    def __organize_parameters_for_custom_script(self, dict_parameters, dict_general, logger=None):
        """Arrange parameters to pass"""
        parameters_str = ''
        if dict_parameters.get('PARAMETERS') == None \
                or dict_parameters.get('PARAMETERS') == '':
            logger.info('No specific parameters found for this module')
            # return None
        else:
            for parameter in dict_parameters['PARAMETERS']:
                if dict_parameters['PARAMETERS'].get(parameter) != None \
                        and dict_parameters['PARAMETERS'].get(parameter) != '':
                    if dict_parameters.get('PARAMETERS_MODE') != 'flat':
                        if parameter == 'TARGETS':
                            dict_parameters['PARAMETERS']['OBJECTIVES'] = dict_parameters['PARAMETERS'].pop(parameter)
                            parameter = 'OBJECTIVES'
                        parameters_str += '--' + parameter + ' "' + dict_parameters['PARAMETERS'][parameter] +'" '
                        # logger.info('Module specific parameters iteration: ' + parameters_str)
                    else:
                        parameters_str += '"' + dict_parameters['PARAMETERS'][parameter] +'" '
        for general_parameters in dict_general:
            if dict_general.get(general_parameters)!= None \
                    and general_parameters  != '':
                parameters_str += '--' + general_parameters + ' "' + str(dict_general[general_parameters]) +'" '
        # logger.info('General parameters iteration: ' + parameters_str)
        return parameters_str


class DynamicImporter:
    def __init__(self, module_name, class_name):
        """Constructor"""
        self.__module = __import__(module_name,globals(),locals(), [class_name])
        self.__class_name = class_name

    def create_object(self, parameters=None, logger=None):
        my_class = getattr(self.__module, self.__class_name)
        for parameter in parameters:
            if parameter == 'TARGETS':
                parameters['OBJECTIVES'] = parameters.pop(parameter)
        if parameters and not logger:
            instance = my_class(parameters)
        elif parameters and logger:
            instance = my_class(parameters, logger)
        elif logger and not parameters:
            instance = my_class(None, logger)
        else:
            instance = my_class()
        return instance
