cachette
========

INTRODUCTION
------------

`cachette` is a handy tool that facilitates CRUD(create/retrieve/update/delete)
operations on frequently accessed data for daily use. It features:

* Simplicity

Storing data in key/value form makes information access simple.

* Convenience

Data can not only be accessed by an *exact* key, but also by a *fuzzy* one.

For example, the value "324 Water St. New York, NY 10002" mapped by "home address"
can alternatively be retrieved by "ha"(**h**ome **a**ddress).

Besides, the matched data are automatically copied into system clipboard, so that they
can easily be pasted into any desired area.

* Safety

For safety, the clipboard containing the sensitive data will be cleared in 10 seconds.

Without doubt, all data are encrypted by [AES](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard).

As for password, Mac OS users can store one in Keychain(make sure its service name is `cachette`).
Unfortunately, Linux or Windows' users will have to type a password manually(which is
inconvenient), or pass a password as an option(which is unsafe).


USAGE
-----

Basically, the command is: `cachette [OPTION]... [key [value]]`, where
`key` is the key used to be retrieved(fuzzy by default) or updated(exact match),
and `value` is the new value for the given `key`.

All supported options are listed as follows:

* _-a_        list all matched data

* _-d KEY_    delete the data mapped by the key(exact)

* _-D KEY_     delete the data mapped by the key(regex)

* _-e_        exact key match in data retrieval

* _-f FILE_    data file's path(default file is set by environment variable `CACHETTE`)

* _-n_        NOT copy into clipboard in data retrieval(imply "-s")

* _-p PWD_     password for data encryption

* _-s_        show the data in the output

* _-t SEC_     seconds for data to be kept in the clipboard(default is 10, 0 means forever)


EXAMPLES
--------

* List all data(**warning**: unsafe):

    cachette

* List all keys: unsafe):

    cachette -k

* Copy the first(ordered by key) value matched by `key1`(fuzzy) to the system clipboard:

    cachette key1

* List all data matched by `key1`(fuzzy, of course):

    cachette -a key1

* Copy the value matched by `key1`(exact) to the system clipboard:

    cachette -e key1

* Copy the value matched by `key1`(fuzzy), keep it in the system clipboard for 1 minute:

    cachette -t60 key1

* Copy the value matched by `key1`(fuzzy), don't clear the system clipboard:

    cachette -t0 key1

* Copy the value matched by `key1`(fuzzy) to the system clipboard and print it on the screen:

    cachette -s key1

* Only print(NOT copy) the value matched by `key1`(fuzzy):

    cachette -n key1

* Map `key1` to the `value1`:

    cachette key1 value1


* Delete the data mapped by `key1`:

    cachette -d key1


* Delete all the data mapped by regex `^key[1-9]`:

    cachette -D '^key[1-9]'


LICENSE
-------

Copyright 2014-2015 Hui Zheng

Released under the [MIT License](http://www.opensource.org/licenses/mit-license.php).

