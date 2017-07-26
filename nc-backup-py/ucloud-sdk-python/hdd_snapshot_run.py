
#!/usr/bin/env python
# -*- coding: utf-8 -*-

from sdk import UcloudApiClient
from config import *
import sys
import json

#实例化 API 句柄


if __name__=='__main__':
    arg_length = len(sys.argv)
    ApiClient = UcloudApiClient(base_url, public_key, private_key)
    Parameters = {"Action": "CreateUDiskSnapshot",
                  "Region": "cn-north-03",
                  "UDiskId": "eeeb233e-c0d4-489d-8bd8-eb9d939c50c7",
                  "Name": "test_snapshot",
                  "Comment": "test"}
    response = ApiClient.get("/", Parameters );
    print json.dumps(response, sort_keys=True, indent=4, separators=(',', ': '))