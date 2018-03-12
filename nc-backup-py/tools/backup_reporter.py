#!/usr/bin/env python2
"""Create BackupReport and send it."""

import time
from communications.communications import Communications

class BackupReporter:

    """Create BackupReport and send it."""

    def __init__(self, json_dict, successful_execution, size_final, logger=None):
        """Initialize class."""
        # self.__parameters = parameters
        self.__size_final = size_final
        self.__logger = logger
        self.__json_dict = json_dict
        self.__logger.info('Sending report...')
        self.__successful_execution = successful_execution

    def create_post_report(self):
        """Create data for report by POST method."""
        if self.__successful_execution:
            status_backup = '0'
        else:
            status_backup = '1'
        if 'STORAGE' in self.__json_dict:
            storage_name = self.__json_dict['STORAGE']['PARAMETERS']['DESTINATION']
        else:
            storage_name = 'Other Snapshot, private, etc, custom'

        # Send report to BRT this section needs more decoupling of code.
        report_attempt_message = 'Trying to send report to BRT'
        self.__logger.info(report_attempt_message)
        print report_attempt_message
        data_post = {
            'srvname': self.__json_dict['GENERAL']['HOSTNAME'],
            'result': status_backup,
            'bckmethod': 'ncscript-py',
            'size': self.__size_final,
            'log': open(self.__json_dict['GENERAL']['LOG_FOLDER'], 'rb').read(),
            'error': '',
            'destination': storage_name
                     }
        return data_post

    def send_post_report(self):
        """Send post report to a given URL."""
        data_post = self.create_post_report()
        count = 1
        time_retry = 60
        message_config_command = self.__json_dict['GENERAL']['MESSAGE_CONFIG_COMMAND']
        message_config_method = self.__json_dict['GENERAL']['MESSAGE_CONFIG_METHOD']
        while count <= 5:
            request_to_brt = Communications.send_message(
                Communications(),
                data_post,
                message_config_command,
                message_config_method)
            self.__logger.info(
                'Report sent status: ' +
                str(request_to_brt.status_code) +
                ' <===> ' + request_to_brt.reason)
            print 'Response from server:'
            attempt_notification = 'Attempt: ' + str(count)
            print attempt_notification
            self.__logger.info(attempt_notification)
            print (request_to_brt.status_code, request_to_brt.reason)
            self.__logger.info('Server response: ' + str(request_to_brt.status_code) + ' ' + str(request_to_brt.reason))
            # this should make the script wait for 60s (1min), 120s (2min), 360s (6min), 1440s (24min), 7200s (2h)
            time_retry = time_retry * count
            count = count + 1
            if request_to_brt.status_code == 200:
                self.__logger.info('Sent')
                break
            elif request_to_brt.status_code != 200 and count is not 5:
                attempt_failed_notification = 'The attempt to send report failed. Attempt number ' + \
                                              str(count) + ' will be in: ' + str(time_retry/60) + ' minutes.'
                print attempt_failed_notification
                self.__logger.warning(attempt_failed_notification)
                time.sleep(time_retry)
            elif count == 5 and request_to_brt.status_code != 200:
                attempt_failed_notification = 'Last attempt to send report FAILED, please check connectivity to BRT'
                print attempt_failed_notification
                self.__logger.critical(attempt_failed_notification)
                exit(1)
