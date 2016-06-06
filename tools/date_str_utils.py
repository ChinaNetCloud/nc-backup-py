#######################################################
# Class Name S3DatePolicy.py                           #
# Synopsis: Get Days Difference                        #
# +days_diff:list                                      #
# date       Change                     Who            #
# 2016-01-14 Created 		       Randy Yang     #
#######################################################

import time

from datetime import datetime


class DatePolicy:
    # Get days difference
	# arg: date and dateformat
	# ret: list of results for daysdiff
    def __init__(self):
        self.name = 'DatePolicy'

    def days_diff(self, current_date, backup_date, dateformat):
        d1 = datetime.strptime(current_date, dateformat)
        d2 = datetime.strptime(backup_date, dateformat)
        daysDiff = str((d1 - d2).days)
        return daysDiff

    def validate(self, date_text, date_format='%Y%m%d'):
        if len(date_text) == 6:
            date_text = "20" + date_text
        try:
            datetime.strptime(date_text, date_format)
            return True
        except:
            return False

# test code
# obj_date = DatePolicy()
# print(obj_date.validate('20160101'))
