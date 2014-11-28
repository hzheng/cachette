#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AES encrypt/decrypt
"""

import sys
import getpass
import hashlib
import base64
from Crypto.Cipher import AES

# the block size for the cipher object
BLOCK_SIZE = 32

# the padding character
PADDING_CHAR = '\0'


def _create_cipher(password):
    return AES.new(hashlib.sha256(password).digest())


def encrypt(plaintext, key):
    cipher = _create_cipher(key)
    leftover = len(plaintext) % BLOCK_SIZE
    if leftover:
        plaintext += (BLOCK_SIZE - leftover) * PADDING_CHAR
    return base64.b64encode(cipher.encrypt(plaintext))


def decrypt(ciphertext, key):
    cipher = _create_cipher(key)
    return cipher.decrypt(
        base64.b64decode(ciphertext)).rstrip(PADDING_CHAR)


def encrypt_file(file_obj, key):
    input_str = ''.join(file_obj.readlines())
    return encrypt(input_str, key)


def decrypt_file(file_obj, key):
    input_str = ''.join(file_obj.readlines())
    return decrypt(input_str, key)


def main(argv=None):
    from optparse import OptionParser
    usage = "usage: %prog [options] [input_file]"
    parser = OptionParser(usage)
    parser.add_option("-d", action="store_true",
                      dest="decrypt", help="decrypt")
    parser.add_option("-p", dest="password", help="password")
    (options, args) = parser.parse_args(argv)

    key = options.password or getpass.getpass("password: ")
    input_file = sys.stdin
    if args:
        input_file = open(args[0])
    try:
        crypt = decrypt_file if options.decrypt else encrypt_file
        sys.stdout.write(crypt(input_file, key))
    finally:
        if args:
            input_file.close()
    return 0


if __name__ == '__main__':
    sys.exit(main())
