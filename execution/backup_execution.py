import imp
import sys


from os import path

from subprocess_execution import SubprocessExecution


from logs_script.log_handler import LoggerHandlers


class BackupExecutionLogic:
    """Scripts execution logic"""
    def iterate_config_script(self,json_dict, home, logger=None):
        c = 1
        result = []
        for scripts_modules in json_dict:
            log_sring = "Section " + str(c) + ": " + scripts_modules
            print log_sring

            logger.info(log_sring)
            #select the script to execute
            external_execution = self.__execute_selection_of_external_script(json_dict,scripts_modules,home, logger)
            print external_execution
            if external_execution:
                result.append(external_execution)
            c += 1
        return result

    def __execute_selection_of_external_script(self,json_dict, scripts_modules, home_folder, logger=None):
        loaded_scripts = []
        for section in json_dict[scripts_modules]:
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
                # check if file exists
                if path.isfile(module_to_call):
                    log_string = "Loading from file: " + module_to_call
                    print log_string
                    logger.info(log_string)
                if pass_parameters is not None:
                    module_to_call = module_to_call + ' ' + pass_parameters
                    logger.info('Calling module: ' + module_to_call)

                log_string = "List of parameters passed to script: " + module_to_call
                # print log_string
                logger.info(log_string)
                # Execute command
                execution_message = []
                execution_message.append(module_to_call)
                try:
                    out_put_exec = SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    module_to_call, logger)
                    execution_message.append(out_put_exec)
                    for this_part in out_put_exec:
                        if this_part is None or this_part == 'stderr: ':
                            logger.info('No output to show or error reported.')
                        else:
                            logger.info('Output:' + str(this_part))
                    loaded_scripts.append(execution_message)
                except Exception as e:
                    e.args += (execution_message,)
                    loaded_scripts.append(e)
                    raise
            # Load plugins dynamically
            elif section == 'ACTION' and json_dict[scripts_modules][section] == "load":
                path_to_import = json_dict[scripts_modules]['FROM'] + '.' + json_dict[scripts_modules]['FILENAME']
                loading_plugin = 'This is a loadable module (plugin): ' + path_to_import
                print loading_plugin
                logger.info(loading_plugin)
                # parameters_list =
                plugin_object = DynamicImporter(path_to_import, json_dict[scripts_modules]['CLASS'], )
                plugin_object.create_object(json_dict[scripts_modules]['PARAMETERS'])

        return loaded_scripts

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
        if dict_parameters.get('PARAMETERS') == None \
                or dict_parameters.get('PARAMETERS') == '':
            logger.info('No specific parameters found for this module')
            return None
        else:
            # print dict_parameters['PARAMETERS']
            parameters_str = ''
            for parameter in dict_parameters['PARAMETERS']:
                if dict_parameters['PARAMETERS'].get(parameter) != None \
                        and dict_parameters['PARAMETERS'].get(parameter) != '':
                    if dict_parameters.get('PARAMETERS_MODE') != 'flat':
                        parameters_str += '--' + parameter + ' "' + dict_parameters['PARAMETERS'][parameter] +'" '
                        logger.info('Module specific parameters iteration: ' + parameters_str)
                    else:
                        parameters_str += '"' + dict_parameters['PARAMETERS'][parameter] +'" '
            for general_parameters in dict_general:
                if dict_general.get(general_parameters)!= None \
                        and general_parameters  != '':
                    parameters_str += '--' + general_parameters + ' "' + dict_general[general_parameters] +'" '
            logger.info('General parameters iteration: ' + parameters_str)
            return parameters_str


class DynamicImporter:
    def __init__(self, module_name, class_name):
        """Constructor"""
        self.__module = __import__(module_name,globals(),locals(), [class_name])
        self.__class_name = class_name

    def create_object(self, parameters=None):
        my_class = getattr(self.__module, self.__class_name)
        if parameters:
            instance = my_class(parameters)
        else:
            instance = my_class()
        return instance


# class