from Crypto.Cipher import DES

__author__ = 'joeny'

if __name__ == '__main__':
    des = DES.new(b'01234567', DES.MODE_ECB)
    text = b'abcdefgh'
    cipher_text = des.encrypt(text)

    print(cipher_text)
    print(des.decrypt(cipher_text))
