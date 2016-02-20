import commands
from os import path

from importlib import import_module

from backupcmd.commands import backupCommands
from configs.load_json_configs import LoadJsonConfig


command_object = backupCommands.feature_commands(backupCommands())

if command_object.run:
    json_dict = LoadJsonConfig.read_config_file(LoadJsonConfig())

print "Backups execution..."
print "Loading and executing modules from configuration sections"
c = 1
for scripts_modules in json_dict:
    print "Section " + str(c) + ": " + scripts_modules
    c += 1

    # itarate through the json config file loaded to dict.
    for section in json_dict[scripts_modules]:
        # print " Sec: " + section
        if section == 'action' and json_dict[scripts_modules][section] == "execute":
            print "loading module: " + json_dict[scripts_modules][section]
            home_folder = path.dirname(path.abspath(__file__))

            # Load module dynamicallt using inbuilt functions.
            # module_to_import = import_module(json_dict[scripts_modules]['name'] + "." + json_dict[scripts_modules]['name'])

            # Execute module from file
            print commands.getoutput('python ' + home_folder + '/' + json_dict[scripts_modules]['name'] + '/' + json_dict[scripts_modules]['name'] + '.py')