import os


class SizeCalculation:
    def __init__(self, parameters):
        self.parameters_dict = parameters
        print self.parameters_dict['OBJECTIVES']

    def __getDirSize(root_dir):
        size = 0
        for path, dirs, files in os.walk(root_dir):
            for f in files:
                size +=  os.path.getsize( os.path.join( path, f ) )
        return size