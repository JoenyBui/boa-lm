"""
CBC uses a 'black box encoder' as discussed in the lecture

AES is a very common example of this, which is available in the Crypto library

For testing purposes, here is AES and some other, silly, encoders

These, or others might be used to grade your code so your implementation should be independent of the encoder used
"""

from Crypto.Cipher import AES

__author__ = 'joeny'


def non_encoder(block, key):
    """
    A basic encoder that doesn't actually do anything

    :param block:
    :param key:
    :return:
    """

    return pad_bits_append(block, len(key))


def xor_encoder(block, key):
    """


    :param block:
    :param key:
    :return:
    """
    block = pad_bits_append(block, len(key))
    cipher = [b ^ k for b, k in zip(block, key)]
    return cipher


def aes_encoder(block, key):
    """

    :param block:
    :param key:
    :return:
    """
    block = pad_bits_append(block, len(key))
    # the pycrypto library expects the key and block in 8 bit ascii
    # encoded strings so we have to convert from the bit string
    block = bits_to_string(block)
    key = bits_to_string(key)
    ecb = AES.new(key, AES.MODE_ECB)
    return string_to_bits(ecb.encrypt(block))


# this is an example implementation of
# the electronic cookbook cipher
# illustrating manipulating the plaintext,
# key, and init_vec
def electronic_cookbook(plaintext, key, block_size, block_enc):
    """
    Return the ecb encoding of `plaintext

    :param plaintext:
    :param key:
    :param block_size:
    :param block_enc:
    :return:
    """
    cipher = []

    # break the plaintext into blocks
    # and encode each one
    for i in range(len(plaintext) / block_size + 1):
        start = i * block_size
        if start >= len(plaintext):
            break
        end = min(len(plaintext), (i+1) * block_size)
        block = plaintext[start:end]
        cipher.extend(block_enc(block, key))
    return cipher


def cipher_block_chaining(plaintext, key, init_vec, block_size, block_enc):
    """
    Return the cbc encoding of `plaintext`

    :param plaintext: bits to be encoded
    :param key: bits used as key for the block encoder
    :param init_vec: bits used as the initialization vector for the block encoder
    :param block_size: size of the block used by `block_enc`
    :param block_enc: function that encodes a block using `key`
    """
    # Assume `block_enc` takes care of the necessary padding
    # if `plaintext` is not a full block

    # return a bit array, something of the form: [0, 1, 1, 1, 0]

    ###############
    # START YOUR CODE HERE
    def xor(x, y):
        return [xx ^ yy for xx, yy in zip(x, y)]

    cipher = []
    xor_input = init_vec

    for i in range(len(plaintext) / block_size + 1):
        start = i * block_size
        if start >= len(plaintext):
            break

        end = min(len(plaintext), (i + 1) * block_size)
        block = plaintext[start:end]
        input_ = xor(xor_input, block)
        output = block_enc(input_, key)
        xor_input = output
        cipher.extend(output)

    return cipher
    # END OF YOUR CODE
    ####################


###################
# Here are some utility functions
# that you might find useful

BITS = ('0', '1')
ASCII_BITS = 8


def display_bits(b):
    """
    converts list of {0, 1}* to string
    :param b:
    :return:
    """
    return ''.join([BITS[e] for e in b])


def seq_to_bits(seq):
    """


    :param seq:
    :return:
    """
    return [0 if b == '0' else 1 for b in seq]


def pad_bits(bits, pad):
    """
    pads seq with leading 0s up to length pad

    :param bits:
    :param pad:
    :return:
    """
    assert len(bits) <= pad
    return [0] * (pad - len(bits)) + bits


def convert_to_bits(n):
    """
    converts an integer `n` to bit array

    :param n:
    :return:
    """
    result = []
    if n == 0:
        return [0]

    while n > 0:
        result = [(n % 2)] + result
        n = n / 2.0

    return result


def string_to_bits(s):
    """

    :param s:
    :return:
    """
    def chr_to_bit(c):
        return pad_bits(convert_to_bits(ord(c)), ASCII_BITS)

    return [b for group in
            map(chr_to_bit, s)
            for b in group]


def bits_to_char(b):
    """

    :param b:
    :return:
    """
    assert len(b) == ASCII_BITS
    value = 0
    for e in b:
        value = (value * 2) + e
    return chr(value)


def list_to_string(p):
    """

    :param p:
    :return:
    """
    return ''.join(p)


def bits_to_string(b):
    """

    :param b:
    :return:
    """
    return ''.join([bits_to_char(b[i:i + ASCII_BITS]) for i in range(0, len(b), ASCII_BITS)])


def pad_bits_append(small, size):
    """
    as mentioned in lecture, simply padding with
    zeros is not a robust way way of padding
    as there is no way of knowing the actual length
    of the file, but this is good enough
    for the purpose of this exercise

    :param small:
    :param size:
    :return:
    """

    diff = max(0, size - len(small))
    return small + [0] * diff


if __name__ == '__main__':

    def test():
        key = string_to_bits('4h8f.093mJo:*9#$')
        iv = string_to_bits('89JIlkj3$%0lkjdg')
        plaintext = string_to_bits("One if by land; two if by sea")

        cipher = cipher_block_chaining(plaintext, key, iv, 128, aes_encoder)
        assert bits_to_string(cipher) == '\xeaJ\x13t\x00\x1f\xcb\xf8\xd2\x032b\xd0\xb6T\xb2\xb1\x81\xd5h\x97\xa0\xaeogtNi\xfa\x08\xca\x1e'

        cipher = cipher_block_chaining(plaintext, key, iv, 128, non_encoder)
        assert bits_to_string(cipher) == 'wW/i\x05\rJQ]\x05\\\r\x05\x0e_G\x03 @Ilkj3$%/hd\x00\x00\x00'

        cipher = cipher_block_chaining(plaintext, key, iv, 128, xor_encoder)
        assert bits_to_string(cipher) == 'C?\x17\x0f+=sb0O37/7|c\x03 @Ilkj3$%/hd9#$'

    test()
