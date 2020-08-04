from getpass import getpass

import dotenv
from dotenv.main import DotEnv
from Crypto.Cipher import Salsa20
from Crypto.Util.Padding import pad
from base64 import b64encode, b64decode

import utility


class VGTUAuth:

    SECRET = "SECRET"
    USERNAME = "USERNAME"
    PASSWORD = "PASSWORD"
    DOTENV = ".env"

    def __init__(self):
        env = DotEnv(self.DOTENV, verbose=False)
        self.secret = env.get(self.SECRET)
        self.username = env.get(self.USERNAME)
        self.password = env.get(self.PASSWORD)

        if self.username is None or self.password is None:
            self.credentials_prompt()
            if self.secret is not None:
                self.save_credentials_prompt()
        else:
            self.username = self.__decrypt(self.username)
            self.password = self.__decrypt(self.password)

    def to_params(self):
        return {
            'username': self.username,
            'password': self.password
        }

    def credentials_prompt(self):
        self.username = input("Username: ")
        self.password = getpass()

    def save_credentials_prompt(self):
        if utility.confirmation_prompt("Do you want to save the credentials?"):
            dotenv.set_key(self.DOTENV, self.USERNAME, self.__encrypt(self.username))
            dotenv.set_key(self.DOTENV, self.PASSWORD, self.__encrypt(self.password))

    def __encrypt(self, value):
        cipher = Salsa20.new(key=self.__secret())
        value_bytes = bytes(value, 'utf-8')
        ciphertext = cipher.nonce + cipher.encrypt(value_bytes)
        return b64encode(ciphertext).decode('utf-8')

    def __decrypt(self, value):
        nonce_size = 8
        value = b64decode(value)
        nonce, ciphertext = value[:nonce_size], value[nonce_size:]
        cipher = Salsa20.new(key=self.__secret(), nonce=nonce)
        return cipher.decrypt(ciphertext).decode('utf-8')

    def __secret(self):
        block_size = 32
        return pad(bytes(self.secret, 'utf-8'), block_size)[:block_size]




