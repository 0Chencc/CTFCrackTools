#coding=utf-8
'''
{
    author:A先森
    title:字符串转16进制
    detail:经过一名网友提示，故此编写这个插件。也是给一个插件的例子
    type:crypto
}
'''
import binascii
def run(string):
    return binascii.b2a_hex(string)