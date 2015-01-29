#!/usr/bin/env python
"""Cronos - Python module for safely and cleanly using sensitive data in code

__author__ = "Jamshed Vesuna"

Notes:
* SimpleCrypt requires python-dev
"""
from getpass import getuser
from os import path
from sys import platform

import pickle
from simplecrypt import encrypt, decrypt

DBNAME = "db.cronos"

class Cronos():

    def __init__(self, passFile=None):
        if passFile is None:
            osType = self.get_osType()
            if osType == 'osx':
                passFile = '/Users/{0}/.ssh/id_rsa'.format(getuser())
            else:
                passFile = '/home/{0}/.ssh/id_rsa'.format(getuser())
        if path.isfile(DBNAME):
            self.cronosDict = pickle.load(open(DBNAME, 'rb'))
            with open(self.deshift(self.cronosDict[self.shift(DBNAME)])) as f:
                self.encryptKey = self.keyFileCipher(f.read())
        else:
            self.cronosDict = {}
            self.encryptKey = ''
            try:
                with open(passFile) as f:
                    self.encryptKey = self.keyFileCipher(f.read())
            except IOError:
                raise IOError('Please provide a valid password file')
            self.cronosDict[self.shift(DBNAME)] = self.shift(passFile)
            pickle.dump(self.cronosDict, open(DBNAME, 'wb'))

    def get(self, key):
        assert type(key) == str, 'Cronos key must be of type string'
        try:
            return decrypt(self.encryptKey, self.cronosDict[self.shift(key)])
        except KeyError as e:
            self.setVal(key)
            return decrypt(self.encryptKey, self.cronosDict[self.shift(key)])

    def setVal(self, key):
        userVal = raw_input('Enter a value for {0}: '.format(key))
        print('Using key={0}'.format(key))
        print('Using value={0}'.format(userVal))
        cipherVal = encrypt(self.encryptKey, userVal)
        self.cronosDict[self.shift(key)] = cipherVal
        pickle.dump(self.cronosDict, open(DBNAME, 'wb'))

    def keyFileCipher(self, key):
        return key[0::2][::-1]

    def shift(self, key):
        cipher = ''
        for i in key:
            cipher += chr(ord(i) + 100)
        return cipher

    def deshift(self, key):
        cipher = ''
        for i in key:
            cipher += chr(ord(i) - 100)
        return cipher

    def get_osType(self):
        if 'linux' in platform:
            return 'linux'
        elif 'darwin' in platform:
            return 'osx'
