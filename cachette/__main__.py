#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Main module
"""

__author__ = "Hui Zheng"
__copyright__ = "Copyright 2011-2012 Hui Zheng"
__credits__ = ["Hui Zheng"]
__license__ = "MIT <http://www.opensource.org/licenses/mit-license.php>"
__version__ = "0.1"
__email__ = "xyzdll[AT]gmail[DOT]com"


import os
import sys
import getpass
import json
import re

from cachette.aes_crypt import decrypt_file, encrypt


class Cachette(object):

    def __init__(self, cache_file, password):
        self._cache_file = cache_file
        self._password = password

        if not os.path.isfile(cache_file) or os.path.getsize(cache_file) < 2:
            # initialize a non-existent or an nearly-empty file
            with open(cache_file, 'w') as f:
                f.write(encrypt("{}", password))

    def list_all_data(self):
        with open(self._cache_file) as f:
            decrypted = decrypt_file(f, self._password)
            return json.loads(decrypted)

    def retrieve_data(self, key, exact=False):
        json_data = {}
        with open(self._cache_file) as f:
            decrypted = decrypt_file(f, self._password)
            json_data = json.loads(decrypted)
        if exact:
            return json_data[key]
        else:
            for k in sorted(json_data):
                pattern = ".*".join([c for c in key])
                if re.search(pattern, k):
                    return json_data[k]
            raise KeyError(u"{}(fuzzy)".format(key))

    def retrieve_all_data(self, key):
        json_data = {}
        with open(self._cache_file) as f:
            decrypted = decrypt_file(f, self._password)
            json_data = json.loads(decrypted)
        for k in sorted(json_data):
            pattern = ".*".join([c for c in key])
            if re.search(pattern, k):
                yield k, json_data[k]

    def _update_data(self, process_data):
        with open(self._cache_file, 'r+') as f:
            decrypted = decrypt_file(f, self._password)
            json_data = json.loads(decrypted)
            process_data(json_data)
            encrypted = encrypt(
                json.dumps(json_data), self._password)
            f.seek(0)
            f.truncate()
            f.write(encrypted)

    def update_data(self, key, value, comment=None):

        def process_data(data):
            data[key] = (value, comment)

        self._update_data(process_data)

    def del_data(self, key):

        def process_data(data):
            del data[key]

        self._update_data(process_data)

    def del_data_re(self, key_re):

        def process_data(data):
            found = False
            for k in data.keys():
                if re.search(key_re, k):
                    found = True
                    del data[k]
            if not found:
                raise KeyError(u"{}(regex)".format(key_re))

        self._update_data(process_data)


ENCODING = sys.stdin.encoding or "UTF-8"


def encode(unicode_val):
    """Encode the given unicode string as stdin's encoding"""
    if unicode_val is None:
        return None
    if isinstance(unicode_val, basestring):
        return unicode_val.encode(ENCODING)
    else:  # assume iterable
        return map(encode, unicode_val)


def decode_args(args, options):
    """Convert args and options to unicode string"""
    for attr, value in options.__dict__.iteritems():
        if isinstance(value, str):
            setattr(options, attr, value.decode(ENCODING))
    return [arg.decode(ENCODING) for arg in args]


def print_data_set(data, style=False):
    key_color = '\033[95m' if style else ''  # purple
    val_color = '\033[94m' if style else ''  # blue
    cmt_color = '\033[92m' if style else ''  # green
    end_color = '\033[0m' if style else ''

    if isinstance(data, dict):
        data = data.items()
    for key, (value, comment) in data:
        sys.stdout.write("{}{:>30s}{} => {}{}{}".format(
            key_color, encode(key), end_color, val_color,
            encode(value), end_color))
        if comment:
            sys.stdout.write(" {}{{{}}}{}".format(
                cmt_color, encode(comment), end_color))
        sys.stdout.write("\n")


def main(argv=None):
    from optparse import OptionParser
    usage = "usage: %prog [options] cache_file [key [value]]"
    parser = OptionParser(usage)
    parser.add_option("-a", action="store_true", default=False,
                      dest="all_matched", help="show all matched data")
    parser.add_option("-c", dest="comment", help="comment")
    parser.add_option("-d", dest="del_key",
                      help="delete data mapped by the key")
    parser.add_option("-D", dest="del_key_re",
                      help="delete data mapped by the key regex")
    parser.add_option("-e", action="store_true", default=False,
                      dest="exact", help="exact key match")
    parser.add_option("-k", action="store_true", default=False,
                      dest="key_only", help="only show keys")
    parser.add_option("-p", dest="password", help="password")
    parser.add_option("-S", action="store_true", default=False,
                      dest="style", help="stylize output")
    (options, args) = parser.parse_args(argv)
    args = decode_args(args, options)

    arg_len = len(args)
    if arg_len < 1:
        parser.error("cache file not specified")
    elif arg_len > 3:
        parser.error("too many arguments")

    password = options.password or getpass.getpass("password: ")
    cachette = Cachette(args[0], password)
    try:
        if arg_len == 1:  # delete matched data or list all data or keys
            if options.del_key:
                cachette.del_data(options.del_key)
            elif options.del_key_re:
                cachette.del_data_re(options.del_key_re)
            elif options.key_only:
                for key in cachette.list_all_data():
                    sys.stdout.write("{}\n".format(encode(key)))
            else:
                print_data_set(cachette.list_all_data(), options.style)
        elif arg_len == 2:  # fetch one item
            key = args[1]
            if options.all_matched:
                print_data_set(cachette.retrieve_all_data(key), options.style)
            else:
                data = cachette.retrieve_data(key, options.exact)
                if data:
                    sys.stdout.write("{}".format(encode(data[0])))
                else:
                    sys.stderr.write("no matched data\n")
                    return 1
        else:  # (arg_len == 3) update one item
            __, key, value = args
            cachette.update_data(key, value, options.comment)
    except ValueError:
        sys.stderr.write("wrong password or corrupted data\n")
        return 1
    except KeyError as e:
        sys.stderr.write("key not found: {} \n".format(encode(e.message)))
        return 1

    return 0


if __name__ == '__main__':
    sys.exit(main())
