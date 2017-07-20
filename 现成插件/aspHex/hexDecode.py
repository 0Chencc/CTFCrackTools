#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
{
title:hexDecode
author:naiquan
type:crypto
detail:AspHex解密
}
'''
def hexDecode(ciphertext):
    ciphertexts = ciphertext.split('%0x')
    while '' in ciphertexts:
        ciphertexts.remove('')
    result = ''
    for ciphertext in ciphertexts:
        result = result + chr(int(ciphertext,16))
    return result

def main(ciphertext):
    return hexDecode(ciphertext)
