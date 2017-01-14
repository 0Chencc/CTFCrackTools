#coding=utf-8
'''
{
    author:A先森
    title:16进制转字符串
    detail:经过一名网友提示，故此编写这个插件。也是给一个插件的例子
    type:crypto
}
'''
import binascii
def run(string):
    return binascii.a2b_hex(string)