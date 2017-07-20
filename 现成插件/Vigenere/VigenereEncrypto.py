#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
{
Title:VigenereEncrypto
Author:naiquan
Type:crypto
Dialog:key
Detail:维吉利亚密码编码
}
'''
def VigenereEncrypto(plaintext, key):
    ascii='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keylen=len(key)
    ptlen=len(plaintext)
    ciphertext = ''
    i = 0
    while i < ptlen:
        j = i % keylen
        k = ascii.index(key[j])
        m = ascii.index(plaintext[i])
        ciphertext += ascii[(m+k)%26]
        i += 1
    return ciphertext

def main(plaintext,key):
    return VigenereEncrypto(plaintext.replace(" ", "").upper(),key.replace(" ", "").upper())
