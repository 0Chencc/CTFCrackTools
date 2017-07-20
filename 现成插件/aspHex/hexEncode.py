#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
{
title:hexEncode
author:naiquan
type:crypto
detail:AspHex加密
}
'''
def hexEncode(plaintext):
    ciphertext = ''
    for i in range(0,len(plaintext)):
        ciphertext = ciphertext + '%' + hex(ord(plaintext[i]))
    return ciphertext

def main(plaintext):
    return hexEncode(plaintext)
