import requests

class RequestUtil:
    def __init__(self):
        self.session = requests.Session()

    def send_request(self, method, url, **kwargs):
        response = self.session.request(method=method, url=url, **kwargs)
        return response