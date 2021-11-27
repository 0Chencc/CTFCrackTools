#!/usr/bin/env python
# -*- coding: utf-8 -*-

#培根密码解密

def peigenDecrypto(string):
    dicts={'aabbb': 'H', 'aabba': 'G', 'baaab': 'R', 'baaaa': 'Q', 'bbaab': 'Z', 'bbaaa': 'Y', 'abbab': 'N', 'abbaa': 'M', 'babaa': 'U', 'babab': 'V', 'abaaa': 'I', 'abaab': 'J', 'aabab': 'F', 'aabaa': 'E', 'aaaaa': 'A', 'aaaab': 'B', 'baabb': 'T', 'baaba': 'S', 'aaaba': 'C', 'aaabb': 'D', 'abbbb': 'P', 'abbba': 'O', 'ababa': 'K', 'ababb': 'L', 'babba': 'W', 'babbb': 'X'}
    sums=len(string)
    j=5   ##每5个为一组
    returnStr = ''
    for i in range(sums/j):
        result=string[j*i:j*(i+1)].lower()
        returnStr = returnStr + dicts[result]
    return returnStr
def author_info():
    info = {
    'name':'BaconDecode',
    'author':'naiquan',
    'describe':'BaconDecode',
    }
def main(string):
    return peigenDecrypto(string)
