from itsdangerous import URLSafeTimedSerializer as utsr
import base64
from base64 import b64encode,b64decode
import re
import json
from pyuan.settings import  SECRET_KEY

class email_token():
    def __init__(self,sk=SECRET_KEY):
        # sk =sk.lstrip('*')
        # sk = sk.replace('+','')
        self.sk = sk
        a = bytes(sk,'utf-8')
        self.salt = base64.encodestring(a).decode().replace('\n','')
    def generate_validate_token(self, username):
        serializer = utsr(self.sk)
        return serializer.dumps(username, self.salt)
    def confirm_validate_token(self,token,expiration=3600):
        serializer = utsr(self.sk)
        return serializer.loads(token, salt=self.salt, max_age=expiration)