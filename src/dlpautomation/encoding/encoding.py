import hashlib
import itertools
import base64
import urllib.parse
import codecs
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
from Crypto.Random import get_random_bytes
from cryptography.fernet import Fernet
import zlib
import logging
from Crypto.Util.Padding import pad


# XOR Encryption
def xor_crypt(data, key):
    logging.debug("XOR Encrypting data with key: {}".format(key))
    key = itertools.cycle(key)
    encrypted_data = [chr(ord(char) * ord(next(key))) for char in data]
    return ''.join(encrypted_data)

# B64 Encryption
def b64_encrypt(data):
    logging.debug("B64 Encrypting data")
    return base64.b64encode(data.encode())

# URL Encoding
def url_encode(data):
    logging.debug("URL Encoding data")
    return urllib.parse.quote(data)

# Hexadecimal Encoding
def hex_encode(data):
    logging.debug("Hex Encoding data")
    return data.encode('utf-8').hex()

# ROT13 Encoding
def rot13_encode(data):
    logging.debug("rot13 Encoding data")
    return codecs.encode(data, 'rot_13')

# ASCII Encoding
def ascii_encode(data):
    logging.debug("ASCII Encoding data")
    return ' '.join(str(ord(c)) for c in data)

# Binary Encoding
def binary_encode(data):
    logging.debug("Binary Encoding data")
    return ' '.join(format(ord(i), '08b') for i in data)

# Caesar Cipher
def caesar_encrypt(data, shift=3):
    logging.debug("Caesar Cipher Encrypting data with shift: {}".format(shift))
    result = ""

    # traverse text
    for i in range(len(data)):
        char = data[i]

        # Encrypt uppercase characters
        if (char.isupper()):
            result += chr((ord(char) + shift - 65) % 26 + 65)

        # Encrypt lowercase characters
        else:
            result += chr((ord(char) + shift - 97) % 26 + 97)

    return result

# Reverse Cipher
def reverse_cipher(data):
    logging.debug("Reverse Cipher Encrypting data")
    return data[::-1]

# AES Encryption - requires key len of 16
def aes_encrypt(data, key):
    logging.debug("AES Encrypting data with key: {}".format(key))
    key = key.encode()  # Convert key to bytes
    if isinstance(data, str):
        data = data.encode()  # Convert data to bytes if it's a string
    cipher = AES.new(key, AES.MODE_ECB)
    ciphertext = cipher.encrypt(pad(data, AES.block_size))  # Pad the data and encrypt it
    return ciphertext.decode('latin-1')  # Return the ciphertext as a 'latin-1' string


# Fernet Encryption - requires key len of 32
def fernet_encrypt(data, keystr):
    key_bytes = hashlib.sha256(keystr.encode()).digest()  # Hash the string to get 32 bytes
    key = base64.urlsafe_b64encode(key_bytes)  # Base64-encode the bytes
    logging.debug("Fernet Encrypting data with key: {}".format(key))
    f = Fernet(key)
    encrypted = f.encrypt(data.encode())  # Data must be bytes
    return encrypted.decode()  # Convert the encrypted bytes to a string

# base32 encode
def base32_encode(data):
    logging.debug("Base32 Encoding data")
    return base64.b32encode(data.encode())

# base16 encode
def base16_encode(data):
    logging.debug("Base16 Encoding data")
    return base64.b16encode(data.encode())

# zlib compression
def zlib_compress(data):
    logging.debug("Zlib Compressing data")
    return zlib.compress(data.encode())




