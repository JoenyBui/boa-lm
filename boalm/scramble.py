import hashlib

from Crypto.PublicKey import RSA

__author__ = 'joeny'


if __name__ == '__main__':
    m = hashlib.md5()
    m.update(b"Nobody inspects")
    print(m.digest())

    key = RSA.generate(2048)
    print(key.exportKey('PEM'))
