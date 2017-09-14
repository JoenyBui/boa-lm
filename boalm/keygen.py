from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, dsa, padding
from cryptography.fernet import Fernet
from cryptography.exceptions import InvalidSignature

__author__ = 'joeny'


class _KeyBase(object):
    """

    """
    def __init__(self, key=None, pubkey=None, secret=None):
        """

        :param key:
        :param pubkey:
        :param secret:
        :return:
        """
        self.key = key

        # A randomize hash key.
        self.hash_key = None

        self.pubkey = pubkey
        self.secret = secret
        self.signature = None

        # The pair key and file given to user.
        self.encrypted_key = None
        self.encrypted_file = None

    def open_private_key(self, filename, password=None):
        """

        :param filename:
        :param password:
        :return:
        """
        with open(filename, 'r') as data_file:
            self.load_private_key(data_file.read(), password)

    def load_private_key(self, key, password=None):
        """

        :param key:
        :param password:
        :return:
        """
        self.key = serialization.load_pem_private_key(
            key,
            password=password,
            backend=default_backend()
        )

    def open_public_key(self, filename):
        """

        :param filename:
        :return:
        """
        with open(filename, 'r') as data_file:
            self.load_public_key(data_file.read())

    def load_public_key(self, key):
        """

        :param key:
        :return:
        """
        self.pubkey = serialization.load_pem_public_key(
            key,
            backend=default_backend()
        )

    def sign_msg(self, msg):
        """
        Sign the message.

        :param msg:
        :return:
        """
        signer = self.key.signer(
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        signer.update(msg)

        self.signature = signer.finalize()

    def sign_key(self):
        """
        Sign encrypted key.

        :return:
        """
        self.sign_msg(self.encrypted_key)

    def verified_msg(self, signature, msg):
        """
        Verify signature.

        :param signature:
        :param msg:
        :return:
        """

        ret_value = True

        try:
            verifer = self.pubkey.verifier(
                signature,
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

            verifer.update(msg)

            verifer.verify()
        except InvalidSignature as e:
            ret_value = False
        finally:
            return ret_value

    def verified_key(self):
        """
        Verified Key.

        :return:
        """
        return self.verified_msg(self.signature, self.encrypted_key)

    def asymmetric_encrypt_msg(self, msg, key=None):
        """
        Using an asymmetric encryption method with private key.

        :param msg:
        :param key:
        :return:
        """
        public_key = self.pubkey

        return public_key.encrypt(
            msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

    def asymmetric_decrypt_msg(self, msg):
        """
        Using an asymmetric decryption using public key.

        :param msg:
        :return:
        """
        return self.key.decrypt(
            msg,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA1()),
                algorithm=hashes.SHA1(),
                label=None
            )
        )

    def symmetric_encrypt_msg(self, msg):
        """
        Encrypt symmetric msg.

        :param msg:
        :return:
        """
        cipher_suite = Fernet(key=self.hash_key)

        return cipher_suite.encrypt(msg)

    def symmetric_decrypt_msg(self, msg):
        """
        Decrypt symmetric msg.

        :param msg:
        :return:
        """
        cipher_suite = Fernet(key=self.hash_key)

        return cipher_suite.decrypt(msg)


class KeyGenerator(_KeyBase):
    """
    Key Generator Utilize Standard Asymmetric and Symmetric Encryption
    """
    def __init__(self):
        """

        :return:
        """
        _KeyBase.__init__(self)

        self.signer = None

    def private_key(self, password=None):
        """
        Private Key should be kept SECRET and not shared to anyone beside personnel who is generating the license file.

        :param password:
        :return:
        """
        if password:
            pem = self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.BestAvailableEncryption(password=password)
            )
        else:
            pem = self.key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption()
            )

        return pem

    def public_key(self):
        """
        Public Key needs to be embedded inside the program.  Keep it relatively safe.

        :return:
        """
        public_key = self.key.public_key()

        puem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

        return puem

    def generate_rsa_key(self):
        """
        Generate RSA pair key.

        :return:
        """
        self.key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )

    def generate_signer(self):
        """
        A private key can be used to sign a message.  This allows anyone with the
        public key to verify that the message was created by someone who possesses
        the corresponding private key.

        :return:
        """
        if self.key:
            self.signer = self.key.signer(
                padding.PSS(
                    mgf=padding.MGF1(hashes.SHA256()),
                    salt_length=padding.PSS.MAX_LENGTH
                ),
                hashes.SHA256()
            )

    def generate_hash_key(self):
        """
        Generate new hash key for symmetric encryption.

        :return:
        """
        self.hash_key = Fernet.generate_key()

    def generate_secret_key(self):
        """
        Generate secret key.

        :return:
        """
        self.secret = Fernet.generate_key()


class KeyReader(_KeyBase):
    """
    Read the key.

    You need a signature...
    """

    def __init__(self, pubkey=None, secret=None):
        """

        :param pubkey:
        :param secret:
        :return:
        """
        _KeyBase.__init__(self, pubkey=pubkey, secret=secret)
