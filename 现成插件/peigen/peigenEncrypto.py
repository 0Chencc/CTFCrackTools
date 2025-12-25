#!/usr/bin/env python
# -*- coding: utf-8 -*-
# 培根密码加密

def peigenEncrypto(string):
    dicts={ 'H': 'aabbb','G': 'aabba','R': 'baaab','Q': 'baaaa','Z': 'bbaab','Y': 'bbaaa','N': 'abbab', 'M': 'abbaa','U': 'babaa','V': 'babab','I': 'abaaa','J': 'abaab','F': 'aabab','E': 'aabaa','A': 'aaaaa','B': 'aaaab','T': 'baabb','S': 'baaba','C': 'aaaba','D': 'aaabb','P': 'abbbb','O': 'abbba','K': 'ababa','L': 'ababb','W': 'babba','X': 'babbb'}
    returnStr = ''
    for i in range(0,len(string)):
        returnStr = returnStr + dicts[string[i].upper()]
    return returnStr
def author_info():
    info = {
    'name':'BaconEncode',
    'author':'naiquan',
    'describe':'BaconEncode',
    }
    return info
def main(string):
    return peigenEncrypto(string)
