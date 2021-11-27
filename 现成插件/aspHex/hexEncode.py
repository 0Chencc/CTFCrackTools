#!/usr/bin/env python
# -*- coding: utf-8 -*-
#detail:AspHex加密
def hexEncode(plaintext):
    ciphertext = ''
    for i in range(0,len(plaintext)):
        ciphertext = ciphertext + '%' + hex(ord(plaintext[i]))
    return ciphertext
def author_info():
    info = {
    'name':'hexEncode',
    'author':'naiquan',
    'describe':'AspHexEncode',
    }
def main(plaintext):
    return hexEncode(plaintext)
