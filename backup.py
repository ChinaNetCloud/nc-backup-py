from backupcmd.commands import backupCommands
from configs.load_json_configs import LoadJsonConfig
from execution.backup_execution import BackupExecutionLogic


command_object = backupCommands.feature_commands(backupCommands())

if command_object.run:
    json_dict = LoadJsonConfig.read_config_file(LoadJsonConfig())
    nc_backup_py_home = json_dict['GENERAL']['HOME_FOLDER']

print 'Backups execution...'
print 'Loading and executing modules from configuration sections'

execution_script = BackupExecutionLogic.iterate_config_script(BackupExecutionLogic(), json_dict, nc_backup_py_home)
# print execution_script
