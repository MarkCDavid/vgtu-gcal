import requests
from urllib import parse as urlparse

from bs4 import BeautifulSoup

from vgtu_auth import VGTUAuth


class VGTULogin:
    INDEX_URL = 'https://mano.vgtu.lt/'
    LOGIN_URL = 'https://sso.vgtu.lt/module.php/core/loginuserpass.php'
    SAML_URL = 'https://mano.vgtu.lt/sso2/module.php/saml/sp/saml2-acs.php/default-sp'

    @staticmethod
    def get_session():

        auth = VGTUAuth().to_params()
        session = requests.session()

        try:
            auth.update(VGTULogin.__get_generated_url_params(session, VGTULogin.INDEX_URL))
            response = VGTULogin.__authenticate_user(session, auth)
            VGTULogin.__authenticate_saml(response, session)
        except VGTULoginError as error:
            print(error.message)
            return None
        return session

    @staticmethod
    def __authenticate_saml(response, session):
        saml_params = {
            'SAMLResponse': VGTULogin.__get_saml_response(response.text),
            'RelayState': VGTULogin.INDEX_URL
        }
        response = session.post(VGTULogin.SAML_URL, saml_params)
        VGTULogin.__raise_on_invalid_response(response, 'SAML Authentication')

    @staticmethod
    def __authenticate_user(session, auth):
        response = session.post(VGTULogin.LOGIN_URL, auth)
        VGTULogin.__raise_on_invalid_response(response, 'User Authentication')
        return response

    @staticmethod
    def __get_generated_url_params(session, url):
        response = session.get(url)
        VGTULogin.__raise_on_invalid_response(response, f'Generating parameters on {VGTULogin.INDEX_URL}')
        return urlparse.parse_qs(urlparse.urlparse(response.url).query)

    @staticmethod
    def __get_saml_response(html):
        soup = BeautifulSoup(html, 'lxml')
        return soup.find('input', type='hidden')['value']

    @staticmethod
    def __raise_on_invalid_response(response, failed_action):
        if response.status_code != 200:
            raise VGTULoginError(f"Status code: {response.status_code}\nFailed action: {failed_action}")


class VGTULoginError(BaseException):

    def __init__(self, message):
        self.message = message
