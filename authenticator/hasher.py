import base64
from datetime import date, datetime
import hashlib
import jwt
import math
import secrets

from datetime import datetime, timedelta
from django.utils.crypto import constant_time_compare, pbkdf2

RANDOM_STRING_CHARS = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'
SECRET = 'SECRET_KEY'
REFRESH_TOKEN_SECRET = 'REFRESH_TOKEN_SECRET'


def encode_access_token(user):
    payload = {
        'exp': datetime.now() + timedelta(hours=600),
        'iat': datetime.now(),
        'user': user
    }
    return jwt.encode(payload, SECRET, algorithm='HS256')

def encode_refresh_token(user):
    payload = {
        'exp': datetime.now() + timedelta(days=7),
        'iat': datetime.now(),
        'user': user
    }
    return jwt.encode(payload, REFRESH_TOKEN_SECRET, algorithm='HS256')

def decode_refresh_token(token):
    try:
        payload = jwt.decode(token, REFRESH_TOKEN_SECRET, algorithms='HS256')
        return payload
    except (jwt.InvalidSignatureError, jwt.InvalidSignatureError) as e:
        return None

def hash_password(password):
    return PBKDF2PasswordHasher().encode(password)


def check_password(password, encoded):
    return PBKDF2PasswordHasher().verify(password, encoded)


class PBKDF2PasswordHasher:
    algorithm = 'pbkdf2_sha256'
    iterations = 100000
    digest = hashlib.sha256

    def encode(self, password, salt=None, iterations=None):
        salt = salt or self.salt()
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm, iterations, salt, hash)

    def decode(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash,
            'iterations': int(iterations),
            'salt': salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_new = self.encode(
            password, decoded['salt'], decoded['iterations'])
        return constant_time_compare(encoded, encoded_new)

    def salt(self):
        char_count = math.ceil(128 / math.log2(len(RANDOM_STRING_CHARS)))
        return ''.join(secrets.choice(RANDOM_STRING_CHARS) for i in range(char_count))
