import wx

import rsa

__author__ = 'joeny'


if __name__ == '__main__':
    (pubkey, privkey) = rsa.newkeys(512)

    print(pubkey)
    print(privkey)

    message = 'hello Bob!'

    crypto = rsa.encrypt(message, pubkey)

    print(crypto)

    nm = rsa.decrypt(crypto, privkey)

    print(nm)

    """
    The most common way to use RSA with larger files uses a block cypher like AES or DES3 to encrypt the file with a
    random key, then encrypt the random key with RSA. You would send the encrypted file along with the encrypted key to
    the recipient.
    """
    # 1. Generate a random key
    import rsa.randnum
    aes_key = rsa.randnum.read_random_bits(128)

    # 2. Use the key to encrypt the file with AES.

    # 3. Encrpyt the AES key with RSA

    # 4. Send the encrypted file together with encrypted_aes_key

    # 5. The recipient now reverses this process to obtain the encrypted file.

