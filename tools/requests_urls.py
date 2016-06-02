import requests


class RequestServer:
    @staticmethod
    def send_post(url_server, data_to_post):
        response = requests.post(url_server, data_to_post)
        return response