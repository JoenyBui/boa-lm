import os
import bcrypt

from Crypto.Hash import SHA256
from Crypto.Hash import MD5

__author__ = 'joeny'


def check_password(clear_password, password_hash):
    """

    :param clear_password:
    :param password_hash:
    :return:
    """
    return SHA256.new(clear_password).hexdigest() == password_hash


def get_file_checksum(filename):
    """
    Another application is file integrity checking. Many downloadable files include a MD5 checksum to verify the
    integrity of the file once downloaded. Here is the code to calculate the MD5 checksum of a file. We work on
    chunks to avoid using too much memory when the file is large.

    :param filename:
    :return:
    """
    h = MD5.new()
    chunk_size = 8192
    with open(filename, 'rb') as f:
        while True:
            chunk = f.read(chunk_size)
            if len(chunk) == 0:
                break
            h.update(chunk)
        return h.hexdigest()

password = b'cnn'

# Hash a password for the first time, with a randomly-generated salt
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

# gensalt's log_rounds parameter determines the complexity.
# The work factor is 2**log_rounds, and the default is 12
hashed = bcrypt.hashpw(password, bcrypt.gensalt(10))

# Check that an unencrypted password matches one that has
# previously been hashed
if bcrypt.hashpw(password, hashed) == hashed:
    print("It matches")
else:
    print("It does not match")

if __name__ == '__main__':
    """
    It is important to know that a hash function like MD5 is vulnerable to collision attacks. A collision attack is
    when two different inputs result in the same hash output. It is also vulnerable to some preimage attacks found in
    2004 and 2008. A preimage attack is: given a hash h, you can find a message m where hash(m) = h.
    """
    value = SHA256.new(b'abc').hexdigest()

    print(check_password(b'abc', value))

    print(bcrypt.gensalt())
