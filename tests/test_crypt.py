# -*- coding: utf-8 -*-

"""
Test utilities.
"""

from cachette.aes_crypt import encrypt, decrypt, encrypt_file, decrypt_file


plain_cipher_pairs = [
    ("", "this is plain", "VXwsoYyJEy3TiDNeTkNtcqPFBTp65J10oMMFwaVZUNQ="),
    ("abc", "1234567890", "CHdEeaWNUeRaTyEeG33zlFdDAb+wYjP91hpaELRY7Cw="),
    ("password", "1234567890", "kMebm+dblKp1CPArPpjZ6VLpWPiaWURRi/h3ptg0u6A="),
    ("!@B^%v9*0dfjDa1c", "!\ntHi*!@$%1a4B81dciacA&#g12iiamci!R$%FD",
     "wmtyhO33HZwemygMvB/Ov9XDWB3CfTt4P6WU9floDnDT+fsg/jCqknOR2nOQo+GGUDvk"
     "hGDFLCcHGA63bxsBIQ=="),
]


def test_crypt_str(tmpdir):
    for key, plain, cipher in plain_cipher_pairs:
        assert encrypt(plain, key) == cipher
        assert decrypt(cipher, key) == plain


def test_crypt_file(tmpdir):
    for key, plain, cipher in plain_cipher_pairs:
        plain_file = tmpdir.join("plain.txt")
        plain_file.write(plain)
        with open(str(plain_file)) as f:
            assert encrypt_file(f, key) == cipher

        cipher_file = tmpdir.join("cipher.txt")
        cipher_file.write(cipher)
        with open(str(cipher_file)) as f:
            assert decrypt_file(f, key) == plain
