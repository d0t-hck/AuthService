import base64
import hashlib
import os
import math

from django.utils.crypto import RANDOM_STRING_CHARS, constant_time_compare, get_random_string, pbkdf2

def hash_password(password):
    salt = os.urandom(32)
    return PBKDF2PasswordHasher().encode(password, salt)

def check_password(password, encoded):
    return PBKDF2PasswordHasher().verify(password, encoded)

class PBKDF2PasswordHasher:
    algorithm = 'pbkdf2_sha256'
    iterations = 100000
    digest = hashlib.sha256

    def encode(self, password, salt, iterations=None):
        #self._check_encode_args(password,salt)
        iterations = iterations or self.iterations
        hash = pbkdf2(password, salt, iterations, digest=self.digest)
        hash = base64.b64encode(hash).decode('ascii').strip()
        return "%s$%d$%s$%s" % (self.algorithm,iterations,salt,hash)
    
    def decode(self, encoded):
        algorithm, iterations, salt, hash = encoded.split('$', 3)
        assert algorithm == self.algorithm
        return {
            'algorithm': algorithm,
            'hash': hash,
            'iterations': iterations,
            'salt': salt,
        }

    def verify(self, password, encoded):
        decoded = self.decode(encoded)
        encoded_new = self.encode(password, decoded['salt'], int(decoded['iterations']))
        return constant_time_compare(encoded, encoded_new)

    def _check_encode_args(self, password, salt):
        if password is None:
            raise TypeError('password must be provided.')
        if not salt or '$' in salt:
            raise ValueError('salt must be provided and canot contain $.')

    def salt(self):
        char_count = math.ceil(128 / math.log2(len(RANDOM_STRING_CHARS)))
        return get_random_string(char_count, allowed_chars=RANDOM_STRING_CHARS)
