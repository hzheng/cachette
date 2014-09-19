#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
AES encrypt/decrypt
"""

__author__ = "Hui Zheng"
__copyright__ = "Copyright 2011-2012 Hui Zheng"
__credits__ = ["Hui Zheng"]
__license__ = "MIT <http://www.opensource.org/licenses/mit-license.php>"
__version__ = "0.1"
__email__ = "xyzdll[AT]gmail[DOT]com"


import sys
import getpass
import hashlib
import base64
from Crypto.Cipher import AES

# the block size for the cipher object
BLOCK_SIZE = 32

# the padding character
PADDING = '\0'


def _create_cipher(password):
    return AES.new(hashlib.sha256(password).digest())


def encrypt(plaintext, key):
    cipher = _create_cipher(key)
    pad = (BLOCK_SIZE - len(plaintext) % BLOCK_SIZE) * PADDING
    return base64.b64encode(cipher.encrypt(plaintext + pad))


def decrypt(ciphertext, key):
    cipher = _create_cipher(key)
    return cipher.decrypt(base64.b64decode(ciphertext)).rstrip(PADDING)


def encrypt_file(file_obj, key):
    input = ''.join(file_obj.readlines())
    return encrypt(input, key)


def decrypt_file(file_obj, key):
    input = ''.join(file_obj.readlines())
    return decrypt(input, key)


def main(argv=None):
    from optparse import OptionParser
    usage = "usage: %prog [options] [input_file]"
    parser = OptionParser(usage)
    parser.add_option("-d", action="store_true",
            dest="decrypt", help="decrypt")
    parser.add_option("-p", dest="password", help="password")
    (options, args) = parser.parse_args(argv)

    key = options.password or getpass.getpass("password: ")
    input = sys.stdin
    if args:
        input = open(args[0])
    try:
        crypt = decrypt_file if options.decrypt else encrypt_file
        sys.stdout.write(crypt(input, key))
    finally:
        if args:
            input.close()
    return 0

if __name__ == '__main__':
    sys.exit(main())
