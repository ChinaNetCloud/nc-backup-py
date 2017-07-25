import logging
import time
import sys


# My own Includes.
from logs_script.log_handler import LoggerHandlers
from backupcmd.commands import backupCommands
from configs.load_json_configs import LoadJsonConfig
from execution.backup_execution import BackupExecutionLogic
from communications.communications import Communications
from tools.os_works import OSInformation
from execution.config_parser import ConfigParser


# Read execution parameters
command_object = backupCommands.feature_commands(backupCommands())

# Determine if running on windows or Linux and sed the default path to configs.
os_name = OSInformation.isWindows()
if (os_name):
    config_file_location = 'conf\\confw.json'
else:
    import fcntl
    if not command_object.config:
        config_file_location = 'conf/conf.json'
    else:
        config_file_location = command_object.config

#Read configurations from JSON
json_dict = LoadJsonConfig.read_config_file(LoadJsonConfig(), config_file_location)

#Check that the Configuration execution does not return an error string.
if not ConfigParser.check_dict_read_is_str(ConfigParser(),json_dict):
    print 'Unexpected error, the config file was supposed to be loaded in a dictionary. Got this instead:'
    print json_dict

# Set logging level of the whole execution. CRITICAL, WARINIG, INFO
def determine_log_level_this_run(command_object):
    if not command_object.logging_level \
            or command_object.logging_level == 'WARINIG' \
            or command_object.logging_level == 'warning':
        logging_level = logging.WARNING
    elif command_object.logging_level == 'INFO' or  command_object.logging_level == 'info':
        logging_level = logging.INFO
    elif  command_object.logging_level == 'CRITICAL' or  command_object.logging_level == 'critical':
        logging_level = logging.CRITICAL
    else:
        logging_level = logging.WARNING
    return logging_level

print json_dict

# Logger object creation.
logger = LoggerHandlers.login_to_file(LoggerHandlers(),'ncbackup', determine_log_level_this_run(command_object),
                                      json_dict['GENERAL']['LOG_FOLDER'],
                                      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# Parse dictionary.
json_dict = ConfigParser.validator_basic(ConfigParser(), json_dict, logger)

# Set the backup as failed by default.
successful_execution = False


# Section to permit only a single instance of the process
if (os_name):
    print 'is windows'
else:
    # Allow only one process to run at the time
    pid_file = json_dict['GENERAL']['HOME_FOLDER'] + '/backup.pid'
    fp = open(pid_file, 'w')
    try:
        fcntl.lockf(fp, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except IOError:
        # another instance is running
        not_multi_thread = 'There is already and instance of this process being executed.'
        logger.critical(not_multi_thread)
        print not_multi_thread
        sys.exit(0)

# Check dict and start execution
if type(json_dict) is not str:
    # start the execution
    if json_dict is not None or type(json_dict) is not str:
        nc_backup_py_home = json_dict['GENERAL']['HOME_FOLDER']
        logger.info('Backups execution...')
        logger.info('Loading and executing modules from configuration sections')
        logger.info('Iterating configs')

        # This is the ACTUAL execution of the different scripts and plugin modules
        # but also executes the preparations for it
        execution_scripts_result = BackupExecutionLogic.iterate_config_script(BackupExecutionLogic(), json_dict,
                                                                      nc_backup_py_home, logger)
        # logger.info('Config itaration done')
        successful_execution = True

    # the size checkups should be removed from here in the future. Ned to think if a less decoupled way.
    # this code takes the execution results and iterates it to find ot problems with all the return codes and messages.
    # this needs A LOT OF WORK still.
    size_final = 'N/A' # Not aplicable, means the script does not have size.
    for script_result in execution_scripts_result:
        if type(script_result[0]) is dict:
            if 'plugin' in script_result[0]:
                if 'size' in script_result[0]['plugin']:
                    size_final = script_result[0]['plugin']['size']
                    successful_execution = True
                elif 'message' in script_result[0]['plugin'] and script_result[0]['plugin']['message'] is not None:
                    if script_result[0]['plugin'].get('message'):
                        if script_result[0]['plugin']['message'][0] == 0:
                            successful_execution = True
                        else:
                            successful_execution = False
                            break
                    else:
                        successful_execution = False
                        break
                else:
                    pass
            elif script_result[0].get('plugin')  and not script_result[0]['plugin'].get('message')\
                    or script_result[0].get('plugin') and not script_result[0]['plugin'].get('size'):
                pass
            elif 'external' in script_result[0] and \
                            'message' in script_result[0]['external'] and \
                            script_result[0]['external']['message'][0] == 0:
                successful_execution = True
            elif 'external' in script_result[0] and \
                            'message' in script_result[0]['external'] and \
                            script_result[0]['external']['message'][0] == 1 and \
                            script_result[0]['external']['message'][2] == 'stderr: No space left':
                successful_execution = False
                print 'No Space left for backups'
            else:
                successful_execution = False
                script_warning = 'Warning:' + str(script_result)
                print script_warning
                print '\nFAILED: Please check the logs for more troubleshooting information or run with ' \
                      '-l INFO enabled to get Full logs\n'
                logger.warning(script_warning)
                break
        else:
            script_result_error = 'One of the scrits retuned a non zero result pease check the logs'
            print script_result_error
            logger.warning(script_result_error)
            successful_execution = False

    logger.info('Sending report...')

    # Here we send the report.
    # It would be good to find a way to move this away from here
    # so the script does not have to Report necesarity
    #ALSO need to implement retries in e.g in 5, 20, 1h 4h, then fail (log everything)
    if successful_execution == True :
        status_backup = '0'
    else:
        status_backup = '1'
    if 'STORAGE' in json_dict:
        storage_name = json_dict['STORAGE']['PARAMETERS']['DESTINATION']
    else:
        storage_name = 'Other Snapshot, private, etc, custom'

    # Send report to BRT this section needs more decoupling of code.
    report_attempt_message = 'Trying to send report to BRT'
    logger.info(report_attempt_message)
    print report_attempt_message
    data_post = {
        'srvname': json_dict['GENERAL']['HOSTNAME'],
        'result': status_backup,
        'bckmethod': 'ncscript-py',
        'size': size_final,
        'log': open(json_dict['GENERAL']['LOG_FOLDER'], 'rb').read(),
        'error': '',
        'destination': storage_name
                 }
    count=1
    time_retry = 60
    message_config_command = json_dict['GENERAL']['MESSAGE_CONFIG_COMMAND']
    message_config_method = json_dict['GENERAL']['MESSAGE_CONFIG_METHOD']
    while count <= 5:
        request_to_brt = Communications.send_message(Communications(), data_post, message_config_command,
                                                     message_config_method)
        logger.info('Report sent status: ' + str(request_to_brt.status_code) + ' <===> ' + request_to_brt.reason)
        print 'Response from server:'
        attempt_notification = 'Attempt: ' + str(count)
        print attempt_notification
        logger.info(attempt_notification)
        print (request_to_brt.status_code, request_to_brt.reason)
        logger.info('Server response: ' + str(request_to_brt.status_code) + ' ' + str(request_to_brt.reason))
        # this should make the script wait for 60s (1min), 120s (2min), 360s (6min), 1440s (24min), 7200s (2h)
        time_retry = time_retry * count
        count = count + 1
        if request_to_brt.status_code == 200:
            logger.info('Sent')
            break
        elif request_to_brt.status_code != 200 and count is not 5:
            attempt_failed_notification = 'The attempt to send report failed. Attempt number ' + \
                                          str(count) + ' will be in: ' + str(time_retry/60) + ' minutes.'
            print attempt_failed_notification
            logger.warning(attempt_failed_notification)
            time.sleep(time_retry)
        elif count == 5 and request_to_brt.status_code != 200:
            attempt_failed_notification = 'Last attempt to send report FAILED, please check connectivity to BRT'
            print attempt_failed_notification
            logger.critical(attempt_failed_notification)
            exit(1)

elif type(json_dict) is str:
    logger.critical('Execution Error with: ' + json_dict + command_object.config)
else:
    logger.critical('Execution Error with: ' + command_object.config)


# provissional logging feature
from execution.subprocess_execution import SubprocessExecution

command_rotatelogs = 'mv ' + json_dict['GENERAL']['LOG_FOLDER'] + '1 ' + \
                     json_dict['GENERAL']['LOG_FOLDER'] + '2'
execution_rotation_result = SubprocessExecution.main_execution_function(SubprocessExecution(), command_rotatelogs, True)
command_rotatelogs = 'mv ' + json_dict['GENERAL']['LOG_FOLDER'] + ' ' + \
                     json_dict['GENERAL']['LOG_FOLDER'] +'1'
execution_rotation_result = SubprocessExecution.main_execution_function(SubprocessExecution(), command_rotatelogs, True)

# End of execution
logger.info('Execution ends here.')
logger = logging.getLogger('ncbackup')
