#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
{
Title:VigenereDecrypto
Author:naiquan
Type:crypto
Dialog:key
Detail:维吉利亚密码解码
}
'''
def vigenereDecrypto(ciphertext,key):
    ascii='ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    keylen=len(key)
    ctlen=len(ciphertext)
    plaintext = ''
    i = 0
    while i < ctlen:
        j = i % keylen
        k = ascii.index(key[j])
        m = ascii.index(ciphertext[i])
        if m < k:
            m += 26
        plaintext += ascii[m-k]
        i += 1
    return plaintext
def main(ciphertext,key):
    return vigenereDecrypto(ciphertext.replace(" ","").upper(),key.replace(" ","").upper())
