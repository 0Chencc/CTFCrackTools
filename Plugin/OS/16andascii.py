#coding=utf-8
import binascii
def ascii216(string):
    return binascii.b2a_hex(string)
def r162ascii(string):
    return binascii.a2b_hex(string)