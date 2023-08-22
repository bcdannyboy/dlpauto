import logging
import string
import random

def genRandomFilename():
    logging.debug("running genRandomFilename()")
    word = ""
    for _ in range(8):
        word += random.choice(string.ascii_letters)
    return word

def adjust_string_length(s, pad_char='X', length=16):
    logging.debug("running adjust_string_length(s=%s, pad_char=%s, length=%d)" % (s, pad_char, length))
    if len(s) > length:
        return s[:length]
    elif len(s) < length:
        return s.ljust(length, pad_char)
    else:
        return s

def rand_string(length=16):
    logging.debug("running rand_string(length=%d)" % length)
    charset = string.ascii_letters + string.digits
    return ''.join(random.choices(charset, k=length))


def byte_to_string(data):
    if isinstance(data, bytes):
        return data.decode('latin-1')
    if isinstance(data, dict):
        return {k: byte_to_string(v) for k, v in data.items()}
    if isinstance(data, list):
        return [byte_to_string(i) for i in data]
    return data

def convert_string_to_ascii_representation(input_string):
    ascii_values = [ord(c) for c in input_string]
    while len(ascii_values) < 4:
        ascii_values.append(0)
    return '.'.join(str(value) for value in ascii_values[:4])

def string_to_ipv6(input_string):
    # Convert each character in the string to its hexadecimal representation
    hex_string = ''.join(format(ord(c), '02x') for c in input_string)

    # Pad the hexadecimal string with zeros if it's less than 32 digits
    hex_string = hex_string.ljust(32, '0')

    # Format the hexadecimal string as an IPv6 address
    ipv6_address = ':'.join(hex_string[i:i+4] for i in range(0, 32, 4))

    return ipv6_address

def can_encode_latin1(s):
    try:
        s.encode('latin-1')
        return True
    except UnicodeEncodeError:
        return False