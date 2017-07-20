#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
{
Title:CaserCode
Author:naiquan
Type:crypto
Detail:凯撒密码
}
'''
def kaisa(lstr):
    returnStr = ''
    for p in range(127):
        str1 = ''
        for i in lstr:
            temp = chr((ord(i)+p)%127)
            if 32<ord(temp)<127 :
                str1 = str1 + temp
                feel = 1
            else:
                feel = 0
                break
        if feel == 1:
            returnStr = returnStr + str1 + '\n'
    return returnStr

def main(lstr):
    print kaisa(lstr)

main('MSTSEC')
