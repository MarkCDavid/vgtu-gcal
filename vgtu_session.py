from bs4 import BeautifulSoup

from vgtu_login import VGTULogin


class VGTUSession:

    def __init__(self):
        self.csrf = None
        self.last_response = None
        self.session = VGTULogin.get_session()
        if self.session is None:
            print("Invalid session! Further use of the session might lead to unexpected results.")

    def get(self, url, **kwargs):
        self.last_response = self.session.get(url, **kwargs)
        self.csrf = self.__get_csrf(self.last_response.text)
        return self.last_response

    def post(self, url, data=None, json=None, **kwargs):
        if data is None:
            data = {}
        data['_csrf'] = self.csrf
        self.last_response = self.session.post(url, data, json, **kwargs)
        return self.last_response

    @staticmethod
    def __get_csrf(html):
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('meta', attrs={'name': 'csrf-token'})['content']

