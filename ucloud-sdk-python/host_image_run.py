#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json


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
    command_host_image = HddImageRun.file_backup_commands(HddImageRun())

    if command_host_image.FILESET_INCLUDE:
        sys.path.append(command_host_image.HOME_FOLDER)
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters = {"Action": "CreateCustomImage",
                  "Region": "cn-north-03",
                  "UHostId": "uhost-rep4lv",
                  "ImageName": "snp_20160517143845",
                  "Comment": "test"}
    response = ApiClient.get("/", Parameters );
    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))