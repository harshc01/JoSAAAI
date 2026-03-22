import requests
from .config import BASE_URL, HEADERS, RETRY_COUNT, TIMEOUT


class SessionManager:
    def __init__(self):
            self.session = requests.Session()
                    self.session.headers.update(HEADERS)
                            self.viewstate = None
                                    self.eventvalidation = None
                                            self.viewstategenerator = None

    def get_initial_page(self):
        pass
    def extract_hidden_fields(self, html):
        pass

    def postback(self, data):
        pass