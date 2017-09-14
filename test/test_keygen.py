import os
import subprocess

from unittest import TestCase

from boalm.keygen import KeyGenerator, KeyReader

__author__ = 'joeny'

GEN_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEA8ZLCrF7wWkbF7r2gN6MM56z8iO4FJZ/DRnJIMHrnMFvB5LR6
KpUS7cMTKWM5ZQD+dk7+70hwcwLCC8m1u4G7VmnSuRR0bhO1weyjfRhj3msS13Rn
pGpGvtYTsfL0nIep6QRF5MjSw6dVWq9VE46MPbW6Q24lEpz7vF4Yj+cKwrvUzYM4
kfxqCfyXTI3nEVEgwRPrfcpqMAvNzXo29TO4iypSInHEeKEcaGfK3Aae7k6FgJb/
wqVTomBNn7NUmNRhch3OohsE9as0axO0xThYPlJhR2Gg+UlnGbXRcO9uo134SAy8
94BZ06oJfpcx5HvowMBgUyeSFfnWbutU4/p7ywIDAQABAoIBAHSBWj/1faecUGNm
srmCenvVUunbGUJe/beg8C3paExLRIS/gde9k6Z1mW0xfIG47AA08wCGCC1/nARB
YNMwqx/u44D9W3WnLdZ8AREYzTl8nFaqvj1uP/ZTmqYMzWoch5ZoyCihrfxMXH7i
5n4LFpnAZjeVDG4gpcvf+aqVO/xT2EulBfQz+yCxBSOrzQ5c+A4KpO+ijc8Vm+MT
C1n+MoO5c+58ZlKoVMYuyOc0RqRlSMkxgGrFNR2uS7oYVl77wMjUXq/HbrDnQK3a
D0Th5D3cSQCjDLb82k/6NS9ClK+JKrvf1krDKXvTX7B/CNgLC6fv3WMouFZCr7Jy
HNe9TSECgYEA/nWAFx7v6ZI/I3kvTL5ZieTyc52nYt9g+VJ1IRNUO/Lf/7VAjbL0
LDU/xHDGtkdmikGnlkPRwVlYbNh17A1sXwki5WXftg+ZQS7IfZDILblGT/rVoYHc
IyJjxJ8MUa/a9hahHUDPZw2GwLcTjQNoK84SZUKzZ2stni6OjzKbuTsCgYEA8wlI
ZHqS4rV5GCJQyY8SuBmbsIE5JxmxW8Ccb9Wx7mB8N669E8H4Aj/X/EMl0ERigj50
e0Fe5kLx2i6hDWoweSTD3vjX1bQfAobHVs0k7+wLOfFawBJXP6qps4T356XMa4Sr
lYUHmDCInNQgmdjbZo0RSSSauWeB05DZL5YnnrECgYEAuWPaQv4jRUVsAuhT8dHt
Ym4PxvRh88NT39KXy9VNVbAKSz8/HP34sAzLvM99t2gl6S0UcIJQ3FG//u1mXOka
v9LkPcYPS5Hp0nfHUtSdQ9Lsy3CxHM6EGIUBs0s9qnY5TXoHQEzrzuUn/FhmQiLt
Tp0BAg2qr/qCbfD1pJb2pekCgYEA8N7dYcBd/dUv/CxedzWWruGqfUfFliwPrMj8
Apb/ryrvUdycRo2yuL//12PRgVWVcFJn7ZS/cmUdAEnAkuQQwLAgdMeaWpIXPdDI
lg3hsuv1wGqlr8E9ubryUBrT/EFFlbY6vIjJGxvW+d//o5ra8AuV+zENK/4bHMzt
hA1EnTECgYAnbdoqZj2oAQLEHW3vHc9lmu5fY2vbfPBR8PfPanaaBAFc76ntSGM4
lTYxtgDtMVGDRHmJCgcgc43T2mfbHmVpJ8zCRpa1Iw4xBkyyKVYM71ZKJbmHYBLb
sRA3HQJwGbeOPMD9xAxp25n5wRJAsxZDgXOZRx0RPeZA02U1+Utzww==
-----END RSA PRIVATE KEY-----
"""

GEN_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA8ZLCrF7wWkbF7r2gN6MM
56z8iO4FJZ/DRnJIMHrnMFvB5LR6KpUS7cMTKWM5ZQD+dk7+70hwcwLCC8m1u4G7
VmnSuRR0bhO1weyjfRhj3msS13RnpGpGvtYTsfL0nIep6QRF5MjSw6dVWq9VE46M
PbW6Q24lEpz7vF4Yj+cKwrvUzYM4kfxqCfyXTI3nEVEgwRPrfcpqMAvNzXo29TO4
iypSInHEeKEcaGfK3Aae7k6FgJb/wqVTomBNn7NUmNRhch3OohsE9as0axO0xThY
PlJhR2Gg+UlnGbXRcO9uo134SAy894BZ06oJfpcx5HvowMBgUyeSFfnWbutU4/p7
ywIDAQAB
-----END PUBLIC KEY-----
"""

READER_PRIVATE_KEY = """-----BEGIN RSA PRIVATE KEY-----
MIIEogIBAAKCAQEAt6LRm4kBeWOVYP1Y4kaBsqqtPt38F2QUHHzSRuRcvR50ylTD
zBPG9ZIcFxXSNqsZdCYSemkQua2l84op0aijr6v3uQS+Xe7Pda97eiPfZVOBqM9p
FN2k3m8VSRRdN29XFl15KsNMYkC8T85QMuNO2uOtuSYk6vIh1yrqZpPPdp7Pqp7J
loywfDP8GL8xOXr6Y2hLmJOVJ5WoNZ7ABjWwwDaNQXCwvmzxoUbrGFFK0kqNWM44
2mp19GuuREHTioOzXb1HU/S2Ei/VNqerO+PBo42cOpVR13A2A+VbDx34XtZHhl4I
Ow8RBe4t/OEfJY5tNxmcoH1RodQ+UfajpI+ZGwIDAQABAoIBAFiCncz9yDweB43s
Dr9hhHn9UeuPS0Zq8laYwzFwOFLfLyOmn4jpr2gFuIxX9C5tYaNeBmIB6hHU5Lvx
yB5JzjuKA6il5KuZw1zR7A3+5FoOWdxnvBpWinS7zeKfch6aB7u76f72iwaAdUNy
Ca29afCO9NjczcaAVldDVB+E9uYQ7LGBLitoUijwE+t+1/L9Qfy9vquWvqTWaAz0
M2SToauzPDjf9ZekMR+98fHSaWyJ2L5r2C8aUzoagXdVhM3W2VTYQVEe8FYjAfIm
0Kla9PoOyH+wI+XyPjXxWBXGTx1n5dYCDvrGj0hDM5rf+y2opyGqPEK8H55cN5JL
kSBhvuECgYEA3S5WtgSJqa2siQ5nLGtGj9MnujLnORl+9sCWCdQbxMFR2Y0SatPs
+unDWaR0gkyvzIIjdEO8zAjCjHTyCUQTHlAitN4IisCXlt//Bq6D0Y6m+v6tngkL
o9RqZSiWqZDSIvjEwWhmaZCHkN8sbS61PqsRbA2IezwlMg+rfWBPaAUCgYEA1Itn
wDh0cTkI0fZBTHcngZiV7Xvuu3Z2zbKoTLQJujU//Wu4Lcz8T4Ix5Sf4cQDkyL8H
r/rLmTjdZHHs6oDThttYEQoRX19QBFWdgDYDVbv7Y33FopNgOdBvqbHEHZj0+kPy
g4Be/DUIP3IG20h6B8oZpahhlCX8JzW4+/ZcZp8CgYAlcPCwwzfih0nLsap5dHdv
ZVk2ReOqYMyDTLqZU1SYC/mlECJr/xAAsY2mIRav7/dacTU7OzQ8fcchK7LFKsbp
vLsDTwq3Ij8HBUgQg35A/Rr7Jh2RwQo9Y3nXQfWvIprP3LjB3MBpYlPwjDbjDKMV
xrOeTPQrmFTbkpd/E8ydWQKBgB8Q3TJITiS6bGKb9sFhbSHRFqDmi2dVElpQca78
ZauU2uyEkSAIpRxN8FMJO5PwyH/bBBmhs56KpDlpOXKxL7m3V7Dt4soo2T448VNr
EaO3XTAWkwuHNPpepecT+PiusKEt9HYmprD6Z49dh4n4X6tokB/Nq5y5QhNYQSuIoKZ
aLoLAoGAIsj43kGRqJVQYMy7dlJkQxuHNI+8z1g9muagUoF+SiEYANq0d9c2tfrS
6yC8NAS+7XwePJchJT64p8J+fnZqB1Vrjog7LBXUvjkjCbgcm95PLYglOM0MyBIA
nKpfTntxSvu2PSWJE4/wKFGO8qX7VL6FXDevwvzKdyBmxTQkAfk=
-----END RSA PRIVATE KEY-----
"""

READER_PUBLIC_KEY = """-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAt6LRm4kBeWOVYP1Y4kaB
sqqtPt38F2QUHHzSRuRcvR50ylTDzBPG9ZIcFxXSNqsZdCYSemkQua2l84op0aij
r6v3uQS+Xe7Pda97eiPfZVOBqM9pFN2k3m8VSRRdN29XFl15KsNMYkC8T85QMuNO
2uOtuSYk6vIh1yrqZpPPdp7Pqp7JloywfDP8GL8xOXr6Y2hLmJOVJ5WoNZ7ABjWw
wDaNQXCwvmzxoUbrGFFK0kqNWM442mp19GuuREHTioOzXb1HU/S2Ei/VNqerO+PB
o42cOpVR13A2A+VbDx34XtZHhl4IOw8RBe4t/OEfJY5tNxmcoH1RodQ+UfajpI+Z
GwIDAQAB
-----END PUBLIC KEY-----
"""

SECRET_KEY = "kjqrlAp0k_GO_o_7a56gdbZrJxQHN8HlhXirmcXTJhk="

HASH_KEY = ""


class KeyGenTest(TestCase):
    """

    """
    def setUp(self):
        self.source_folder = os.path.dirname(__file__)

        self.keygen = KeyGenerator()
        self.keygen.open_private_key('gen_private.key')
        self.keygen.open_public_key('reader_public.key')
        self.keygen.secret = SECRET_KEY

    def test_generate_rsa_key(self):
        self.keygen.generate_rsa_key()

        msg = b'JaneDoe2001!'
        ciphertext = self.keygen.asymmetric_encrypt_msg(msg)

        self.assertNotEqual(msg, ciphertext)

        self.s = KeyGenerator()
        self.s.load_private_key(self.keygen.private_key())

        self.assertEqual(self.s.asymmetric_decrypt_msg(ciphertext), msg)

    def test_load_key(self):
        self.assertEqual(self.keygen.private_key(), GEN_PRIVATE_KEY, "Private Key is not the same.")
        self.assertEqual(self.keygen.public_key(), GEN_PUBLIC_KEY, "Public Key is not the same.")

    def test_load_public_key(self):
        self.kg = KeyGenerator()
        self.kg.load_public_key(GEN_PUBLIC_KEY)
        self.kg.load_private_key(GEN_PRIVATE_KEY)

        msg = b'JaneDoe2001!'
        ciphertext = self.keygen.asymmetric_encrypt_msg(msg)

        self.assertEqual(msg, self.kg.asymmetric_decrypt_msg(ciphertext))

    def test_symmetric_encryption(self):
        self.keygen.generate_hash_key()

        msg = b"A new secret message."

        cipher_text = self.keygen.symmetric_encrypt_msg(msg)

        self.assertEqual(msg, self.keygen.symmetric_decrypt_msg(cipher_text))

    def test_encrypt_key(self):
        self.keygen.generate_hash_key()


class KeyReaderTest(TestCase):
    """

    """
    def setUp(self):
        self.read = KeyReader()
        self.read.open_private_key('reader_private.key')
        self.read.open_public_key('gen_public.key')
        self.read.secret = SECRET_KEY

        self.kg = KeyGenerator()
        self.kg.open_private_key('gen_private.key')
        self.kg.open_public_key('reader_public.key')
        self.kg.secret = SECRET_KEY
        self.kg.generate_hash_key()
        # self.kg.sign_key()
        
        self.top_secret_msg = "John F. Kennedy was assassin by the CIA."

    def test_verified_key(self):
        signature = None
        with open('signature', 'r') as data_file:
            signature = data_file.readlines()

        print(signature)
        self.read.verified_key(signature[0], self.top_secret_msg)

    def test_sign_key(self):

        old_signature = self.kg.signature

        self.kg.sign_msg(self.top_secret_msg)
        print("New Signautre")
        print(self.kg.signature)

        with open('signature', 'w') as data_file:
            data_file.write(self.kg.signature)

