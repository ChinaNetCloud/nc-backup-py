import logging


from logs_script.log_handler import LoggerHandlers
from backupcmd.commands import backupCommands
from configs.load_json_configs import LoadJsonConfig
from execution.backup_execution import BackupExecutionLogic
from communications.communications import Communications
from tools.os_works import OSInformation



os_name = OSInformation.isWindows()
if (os_name):
    config_file_location = 'conf\\confw.json'
else:
    config_file_location = 'conf/conf.json'

json_dict = LoadJsonConfig.read_config_file(LoadJsonConfig(), config_file_location)
logger = LoggerHandlers.login_to_file(LoggerHandlers(),'ncbackup', 10,
                                      json_dict['GENERAL']['LOG_FOLDER'],
                                      '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

successful_execution = False
try:
    command_object = backupCommands.feature_commands(backupCommands())

except Exception as exceptio_reading_commands:
    logger.critical('The main script did not manage to read the parameters passed by user Exited with: ')
    successful_execution = False

if type(json_dict) is not str:
    if json_dict is not None or type(json_dict) is not str:
        nc_backup_py_home = json_dict['GENERAL']['HOME_FOLDER']
        logger.info('Backups execution...')
        logger.info('Loading and executing modules from configuration sections')
        try:
            logger.info('Iterating configs')
            execution_script = BackupExecutionLogic.iterate_config_script(BackupExecutionLogic(), json_dict,
                                                                          nc_backup_py_home)
            print execution_script
            logger.info('Config itaration done')
            successful_execution = True
        except Exception as exception_executing_external_script:
            logger.critical('The main script did not Execute the backups scripts after loading configs: ')
            successful_execution = False
    if successful_execution:
        logger.info('Sending report...')
        data_post = {'srvname': json_dict['GENERAL']['HOSTNAME'], 'result':'OK', 'bckmethod': 'ncscript', 'size': '10MB', 'log': 'Not in use', 'error': ''}
        a = Communications.send_post(Communications(), data_post)
        logger.info('Report sent status: ' + str(a.status_code) + ' <===> ' + a.reason)
        print (a.status_code, a.reason)
    else:
        logger.critical('Execution Error before sending report.')
elif type(json_dict) is str:
    logger.critical('Execution Error with: ' + json_dict + command_object.config)
else:
    logger.critical('Execution Error with: ' + command_object.config)

logger.info('Execution ends here.')
logger = logging.getLogger('ncbackup')