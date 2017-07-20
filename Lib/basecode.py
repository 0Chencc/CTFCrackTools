#coding=utf-8
#author:A先森
#team:米斯特安全
import base64
def b32e(data):
  encode = base64.b32encode(data)
  return encode
def b32d(data):
  encode = base64.b32decode(data)
  return encode
def b16e(data):
  encode = base64.b16encode(data)
  return encode
def b16d(data):
  decode = base64.b16decode(data)
  return decode