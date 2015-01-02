cronos
======

Python module for safely and cleanly using sensitive data in shared code.

Cronos uses a secure encryption method, [AES256](http://en.wikipedia.org/wiki/Advanced_Encryption_Standard), to store passwords and sensitive values locally. Simple (and unsecure) [Caesar Ciphers](http://en.wikipedia.org/wiki/Caesar_cipher) are used to create obfuscated keys in the cronos datastore. This means keys are simply human-unreadable and values are securely encrypted with a password file (defaults to your ssh private key).

Install
-------
* Python Pip: `pip install cronos`

Usage
-----
While global keys are stored in your code (such as the plaintext `API_KEY` in the examples below), Cronos uses the single interface `get` to *initially* prompt the user for the value at runtime. Cronos stores the encrypted value in a keystore called `db.cronos`. Upon a second call to `get`, Cronos performs a lookup and decryption.

You may want to add `*.cronos` to your `.gitignore`.

Using `mypassword.txt` as the encryption key:
```python
from cronos import Cronos
c = cronos.Cronos('mypassword.txt')
myKey = c.get("API_KEY")  # Prompt user for API_KEY if not already stored
```

Using `id_rsa.pub` as the default encryption key:
```python
from cronos import Cronos
c = cronos.Cronos()
myKey = c.get("API_KEY")  # Prompt user for API_KEY if not already stored
```

Requirements
------------
* [getpass](https://docs.python.org/2/library/getpass.html)
* [os](https://docs.python.org/2/library/os.html)
* [pickle](https://docs.python.org/2/library/pickle.htmlpassword)
* [simplecrypt](https://pypi.python.org/pypi/simple-crypt)
