# -*- coding: utf-8 -*-

"""
Test main functions.
"""

import re
import tempfile

import pytest

from cachette.__main__ import Cachette

sample_key_vals = {
    "key0": [None, None],
    "key1": ["value1", None],
    "key2": [None, "comment 2"],
    "key2a": ["value2a", "comment 2a"],
    "key3": ["value3", "comment 3"],
    "_key4": ["value4", "comment 4"],
    "!key5": ["value5", "comment 5"],
    "Key6": ["value6", "comment 6"],
}


@pytest.fixture(scope="module")
def cachette():
    cache_file = tempfile.mkstemp()[1]
    password = "my_secret_key"
    return Cachette(cache_file,  password)


def test_update(cachette):
    assert cachette.list_all_data() == {}

    for key, (val, comment) in sample_key_vals.items():
        cachette.update_data(key, val, comment)
        assert cachette.retrieve_data(key, True) == [val, comment]

    assert cachette.list_all_data() == sample_key_vals


def test_retrieve(cachette):
    assert cachette.list_all_data() == sample_key_vals
    assert cachette.retrieve_data("k") == cachette.retrieve_data("!key5")
    assert cachette.retrieve_data("ky") == cachette.retrieve_data("!key5")
    assert cachette.retrieve_data("k1") == cachette.retrieve_data("key1")
    assert cachette.retrieve_data("ky1") == cachette.retrieve_data("key1")
    assert cachette.retrieve_data("k2") == cachette.retrieve_data("key2")
    assert cachette.retrieve_data("ky2") == cachette.retrieve_data("key2")
    assert cachette.retrieve_data("K") == cachette.retrieve_data("Key6")
    with pytest.raises(KeyError):
        cachette.retrieve_data("K1")
    with pytest.raises(KeyError):
        cachette.retrieve_data("k1", True)

    all_k = list(cachette.retrieve_all_data("k"))
    all_k.sort()
    samples = [(k, v) for (k, v) in sample_key_vals.items() if "k" in k]
    samples.sort()
    assert all_k == samples


def test_delete(cachette):
    assert cachette.list_all_data() == sample_key_vals

    tmp_key_vals = dict(sample_key_vals)
    for key in sample_key_vals.keys():
        cachette.del_data(key)
        del tmp_key_vals[key]
        assert cachette.list_all_data() == tmp_key_vals

    assert cachette.list_all_data() == {}


def test_delete_re(cachette):
    test_update(cachette)
    key_re = "key."
    cachette.del_data_re(key_re)
    assert cachette.list_all_data() == {
        k: v for (k, v) in sample_key_vals.items() if not re.search(key_re, k)}

    with pytest.raises(KeyError):
        cachette.del_data_re(key_re)
