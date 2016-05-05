from os import path

from subprocess_execution import SubprocessExecution


from logs_script.log_handler import LoggerHandlers


class BackupExecutionLogic:
    """Scripts execution logic"""
    def iterate_config_script(self,json_dict, home, logger=None):
        c = 1
        result = []
        # self.__logger = LoggerHandlers.login_to_file(LoggerHandlers(), 'ncbackup', 10,
        #                                       json_dict['GENERAL']['LOG_FOLDER'],
        #                                       '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
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
            if section == 'ACTION' and json_dict[scripts_modules][section] == "execute":
                log_string = "loading executable module: " + json_dict[scripts_modules]['NAME']
                print log_string
                logger.info(log_string)
                module_to_call = self.__prepare_configs_for_execution(json_dict,scripts_modules,home_folder)
                pass_parameters = self.__organize_parameters_for_custom_script(json_dict[scripts_modules],json_dict['GENERAL'])
                # check if file exists
                if path.isfile(module_to_call):
                    log_string = "Loading from file " + module_to_call
                    print log_string
                    # logger.info(log_string)
                if pass_parameters is not None:
                    module_to_call = module_to_call + ' ' + pass_parameters
                    # print module_to_call
                    # exit(0)
                log_string = "List of parameters passed to script: " + module_to_call
                print log_string
                # logger.info(log_string)
                # Execute command
                execution_message = []
                execution_message.append(module_to_call)
                try:
                    execution_message.append(SubprocessExecution.main_execution_function(SubprocessExecution(),
                                                                                    module_to_call))
                    loaded_scripts.append(execution_message)
                except Exception as e:
                    e.args += (execution_message,)
                    loaded_scripts.append(e)
                    raise
        return loaded_scripts

    def __prepare_configs_for_execution(self, json_dict,scripts_modules,home_folder):
        """Prepare configurations for execution create path, get parameters, etc"""
        call_module = ''
        if json_dict[scripts_modules].get('EXECUTE_WITH') == None \
                or json_dict[scripts_modules].get('EXECUTE_WITH') == '':
            call_module = 'python '
        else:
            call_module = json_dict[scripts_modules]['EXECUTE_WITH'] + ' '

        call_module += home_folder + '/'
        # print call_module
        if json_dict[scripts_modules].get('EXECUTABLE') == None \
                or json_dict[scripts_modules].get('EXECUTABLE') == '':
            json_dict[scripts_modules]['EXECUTABLE'] = json_dict[scripts_modules]['NAME'] + '.py'
        call_module += json_dict[scripts_modules]['NAME'] + '/' + json_dict[scripts_modules]['EXECUTABLE']

        return call_module

    def __organize_parameters_for_custom_script(self, dict_parameters, dict_general):
        """Arrange parameters to pass"""
        if dict_parameters.get('PARAMETERS') == None \
                or dict_parameters.get('PARAMETERS') == '':
            return None
        else:
            # print dict_parameters['PARAMETERS']
            parameters_str = ''
            for parameter in dict_parameters['PARAMETERS']:
                if dict_parameters['PARAMETERS'].get(parameter) != None \
                        and dict_parameters['PARAMETERS'].get(parameter) != '':
                    if dict_parameters.get('PARAMETERS_MODE') != 'flat':
                        parameters_str += '--' + parameter + ' "' + dict_parameters['PARAMETERS'][parameter] +'" '
                    else:
                        parameters_str += '"' + dict_parameters['PARAMETERS'][parameter] +'" '
            for general_parameters in dict_general:
                if dict_general.get(general_parameters)!= None \
                        and general_parameters  != '':
                    parameters_str += '--' + general_parameters + ' "' + dict_general[general_parameters] +'" '
            return parameters_str
