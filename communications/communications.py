from tools.requests_urls import RequestServer

class Communications:
    def send_post(self, data):
        url_brt = 'https://backupreporter.service.chinanetcloud.com/backup_report_service/backup_service.php'
        return RequestServer.send_post(url_brt, data)