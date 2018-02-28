# Files backup

The following is a working example of a section that calls and executes external commands to compress a fileset.

```json
  "FILESET": {
    "ACTION": "execute",
    "NAME": "filesbackup",
    "PARAMETERS": {
      "__READTHIS": "Space delimited paths to backup (recursive)",
      "FILESET_INCLUDE": "/etc /home/user",
      "__READTHIS": "Space delimited paths to exclude (within FILESET_INCLUDE)",
      "FILESET_EXCLUDE": ""
    }
  },
```
Notice: `FILESET_INCLUDE` can not be "/"

## Optional parameters
This section as most of the others have most of it's parameters as optional. For a default Cent OS 6 or 7 configuration this section should work the same as the section before as it would assume default configurations according to our new standards.
```json
      "FILESET":{
        "ACTION": "execute",
        "NAME": "filesbackup"
     }
```

## Parameters
* `"FILESET":` Defines a section beginning, the name can be anything, but as a convention is good to give it a name according to it's content.
* `"ACTION":` "execute", The kay word ACTION says to the script the now I want to say what to do in the section, there are 2 possible options defined for now:
* `execute:` means an external code script is going to be executed.
* `load:` a dynamic module will be loaded. There is a slide but important difference between "execute" and "load", load is to execute native python code in the for of dynamic imports while the other executes external independent scripts that can be done using any programming language as long as it follows some basic rules.
* `"NAME": "filesbackup"`, `NAME` is to specify the name of the folder where to find the plugin or script to load/execute. Is advised to call the modules the same name of the folder, but is not a requirement. Then "filesbackup" is the name of the external script to be executed in this case.
* (Optional) `"EXECUTE_WITH": "python",` Is to know what type of code you need to execute, if your code is python, then you do not need to specify.
* (Optional) `"EXECUTABLE": "",` is to know which one is the executable file in the module.
* (Optional) `"PARAMETERS": {` This subsection is to pass parameters to the module to be executed/loaded. Inside you add parameters that you want the plugin/script to receive.
* (Optional, specific to the plugin or script to load or execute) `"FILESET_INCLUDE": "/etc /Users/cncuser/Documents/",` The parameters are all depending on what you need to execute your code. Every section can have different parameters depending on the way it was programmed.
