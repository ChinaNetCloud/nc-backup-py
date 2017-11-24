#!/usr/bin/env python2
"""Create BackupReport and send it."""

from time import time
from datetime import datetime
from communications.communications import Communications
from smtp_email import sendMail


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
        self.__logfile = self.__json_dict['GENERAL']['LOG_FOLDER']
        self.__hostname = self.__json_dict['GENERAL']['HOSTNAME']
        if "STORAGE" in json_dict:
            self.__destination = self.__json_dict['STORAGE']['PARAMETERS']['DESTINATION']
        with open(self.__logfile, 'rb') as f:
            self.__logtext = f.read()

        if self.__successful_execution:
            self.__status_backup = '0'
        else:
            self.__status_backup = '1'
        if 'STORAGE' in self.__json_dict:
            self.__storage_name = self.__destination
        else:
            self.__storage_name = 'Other Snapshot, private, etc, custom'

        self.__report_time = datetime.utcnow().strftime("%d-%m-%Y %H:%M:%S")

    def execute(self):
        if "MESSAGE_POST" in self.__json_dict.keys():
            self.create_post_report()
            urls = self.__json_dict['MESSAGE_POST']['URLS']
            for url in urls:
                self.send_post_report(url)
        if "MESSAGE_EMAIL" in self.__json_dict.keys():
            self.send_email_report()
        # logger.info('No report(s) enabled in configuration.')

    def create_post_report(self):
        """Create data for report by POST method."""

        data_post = {
            'srvname': self.__hostname,
            'result': self.__status_backup,
            'bckmethod': 'ncscript-py',
            'size': self.__size_final,
            'log': self.__logtext,
            'error': '',
            'destination': self.__storage_name
                     }
        return data_post

    def send_post_report(self, url):
        """Send post report to BRT / a given URL."""

        report_attempt_message = 'Trying to send report to BRT'
        self.__logger.info(report_attempt_message)
        print report_attempt_message

        data_post = self.create_post_report()
        count = 1
        time_retry = 60
        while count <= 5:
            request_to_brt = Communications.send_message(
                Communications(),
                data_post,
                url,
                "post")
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

    def send_email_report(self):

        report_attempt_message = 'Trying to send report to BRT'
        self.__logger.info(report_attempt_message)
        print report_attempt_message

        if self.__status_backup == 0:
            subject = "Sucess! "
        else:
            subject = "Failed! "
        subject += self.__hostname + ' '
        subject += ' Backup Report'
        subject += self.__report_time
        body = "The backup job on %s was %s. Please find the backup log attached to this email." %(self.__hostname, self.__status_backup)
        to = self.__json_dict['MESSAGE_EMAIL']['TO_IDS']
        fro = self.__json_dict['MESSAGE_EMAIL']['FROM_IDS']
        server = self.__json_dict['MESSAGE_EMAIL']['SERVER']
        username = self.__json_dict['MESSAGE_EMAIL']['USERNAME']
        password = self.__json_dict['MESSAGE_EMAIL']['PASSWORD']
        sendMail(to=to, fro=fro,
                 subject=subject, text=body, files=[self.__logfile],
                 server=server,
                 username=username,
                 password=password)
