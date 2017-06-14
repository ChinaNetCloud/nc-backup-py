from tools.requests_urls import RequestServer

class Communications:
    def send_message(self, data, command_line=None, command_mode=None):
        if command_line is None:
            command_line = 'http://localhost'
        if command_mode is None or command_mode == 'post':
            return RequestServer.send_post(command_line, data)