#!/usr/bin/env python
# -*- coding: utf-8 -*-

#detail:AspHex解密
def hexDecode(ciphertext):
    ciphertexts = ciphertext.split('%0x')
    while '' in ciphertexts:
        ciphertexts.remove('')
    result = ''
    for ciphertext in ciphertexts:
        result = result + chr(int(ciphertext,16))
    return result
def author_info():
    info = {
    'name':'hexDecode',
    'author':'naiquan',
    'describe':'AspHexDecode',
    }
def main(ciphertext):
    return hexDecode(ciphertext)
