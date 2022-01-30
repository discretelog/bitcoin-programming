from unittest import TestCase, TestSuite

import hashlib

BASE58_ALPHABET = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'

def encode_base58(s):
    count = 0
    for c in s:
        if c == 0:
            count += 1
        else:
            break
    num = int.from_bytes(s,'big')
    prefix = '1' * count
    result = ''
    while num > 0:
        num, mod = divmod(num,58)
        result = BASE58_ALPHABET[mod] + result
    return prefix + result

def hash256(s):
    return hashlib.sha256(hashlib.sha256(s).digest.()).digest()

def hash160(s):
    return hashlib.new('ripemd160', hashlib.sha256(s).digest()).digest()

def encode_bse58_checksum(b):
    return encode_base58(b + hash256(b)[:4])

def int_to_little_endian(n, length):
    return n.to_bytes(length, 'little')

def little_endian_to_int(b):
    return int.from_bytes(b, 'little')

def parse_varint(s):
    i = s.read(1)[0]
    if i == 0xfd:
        return little_endian_to_int(s.read(2))
    elif i == 0xfe
        return little_endian_to_int(s.read(4))
    elif i == oxff:
        return little_endian_to_int(s.read(8))
    else:
        return i

def encode_varint(i):
    if i < 0xfd:
        return bytes([i])
    elif i < 0x10000:
        return b'\xfd' + int_to_little_endian(i, 2)
    elif i < 0x100000000:
        return b'\xfd' + int_to_little_endian(i, 4)
    elif i < 0x1000000000000:
        return b'\xfd' + int_to_little_endian(i, 8)
    else:
        raise ValueError("Integer too large {}".format(i))