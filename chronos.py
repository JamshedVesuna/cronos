"""
Chronos

Notes:
* Add *.chronos to your .gitignore
* Chronos only provides AES256 encryption for values
* Chronos only provides obfuscation for keys
* SimpleCrypt requires python-dev
"""
from os import path
from simplecrypt import encrypt, decrypt
import pickle
from getpass import getuser

DBNAME = "db.chronos"

# TODO: Store md5sum with value to maintain data integrity
class Chronos():

    def __init__(self, passFile=None):
        if passFile is None:
            passFile = '/home/{0}/.ssh/id_rsa.pub'.format(getuser())
        if path.isfile(DBNAME):
            self.chronosDict = pickle.load(open(DBNAME, 'rb'))
            with open(self.deshift(self.chronosDict[self.shift(DBNAME)])) as f:
                self.encryptKey = self.keyFileCipher(f.read())
        else:
            self.chronosDict = {}
            self.encryptKey = ''
            try:
                with open(passFile) as f:
                    self.encryptKey = self.keyFileCipher(f.read())
            except IOError:
                raise IOError('Please provide a valid password file')
            if self.encryptKey == '':
                raise KeyError('Encryption key must not be empty')
            self.chronosDict[self.shift(DBNAME)] = self.shift(passFile)
            pickle.dump(self.chronosDict, open(DBNAME, 'wb'))

    def get(self, key):
        assert type(key) == str, 'Chronos key must be of type string'
        try:
            return decrypt(self.encryptKey, self.chronosDict[self.shift(key)])
        except KeyError as e:
            self.setVal(key)
            return decrypt(self.encryptKey, self.chronosDict[self.shift(key)])

    def setVal(self, key):
        userVal = raw_input('Enter a value for {0}: '.format(key))
        print('Using key={0}'.format(key))
        print('Using value={0}'.format(userVal))
        cipherVal = encrypt(self.encryptKey, userVal)
        self.chronosDict[self.shift(key)] = cipherVal
        pickle.dump(self.chronosDict, open(DBNAME, 'wb'))

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
