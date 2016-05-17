from sdk import UcloudApiClient
from config import *
import sys
import json


import time
import argparse

#实例化 API 句柄
class HddImageRun:


    def hdd_image_commands(self):
        parser_object = argparse.ArgumentParser()
        parser_object.add_argument('-R', '--REGION', type=str
                                   , help='Script home folder required(from where the master script runs)', required=True)
        parser_object.add_argument('-o', '--HOST_ID', type=str
                                   , help='This is the folder to use for temporary files works', required=True)
        parser_object.add_argument('-H', '--HOME_FOLDER', type=str
                                   , help='Script home folder required(from where the master script runs)',
                                   required=True)
        args_list, unknown = parser_object.parse_known_args()
        return args_list


if __name__=='__main__':
    command_host_image = HddImageRun.hdd_image_commands(HddImageRun())

    if command_host_image.REGION:
        sys.path.append(command_host_image.HOME_FOLDER)
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    datetime_string = time.strftime("%Y%m%d_%H%M%S")

    Parameters = {"Action": "CreateCustomImage",
                  "Region": command_host_image.REGION,
                  "UHostId": command_host_image.HOST_ID,
                  "ImageName": "img_" + datetime_string + command_host_image.HOST_ID,
                  "Comment": "Backup for: " + command_host_image.HOST_ID + " Region: " + command_host_image.REGION + "Host ID:" + command_host_image.HOST_ID }
    response = ApiClient.get("/", Parameters );
    result_execution = json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))
    print result_execution
    if result_execution['RetCode'] != 0:
        print 'return code different than 0, script has failed'
        exit(1)