# CTFcrackTools-V3.2
[![Build Status](https://travis-ci.org/0Chencc/CTFCrackTools.svg?branch=master)](https://travis-ci.org/0Chencc/CTFCrackTools)
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://raw.githubusercontent.com/0Chencc/CTFCrackTools/master/doc/LICENSE)
[![language](https://img.shields.io/badge/Language-Java/Kotlin-orange.svg)](https://github.com/0Chencc/CTFCrackTools/)

作者：林晨(0chen)

米斯特安全官网：http://www.acmesec.cn/

## 第二版
应老用户要求，将继续更新V2版本。以下是项目地址：

[https://github.com/Acmesec/CTFCrackTools-V2](https://github.com/Acmesec/CTFCrackTools-V2)

## 界面介绍

![mark](/img/use.gif)

## 框架介绍

使用kotlin与java混合开发

这大概是国内首个应用于CTF的工具框架。

可以被应用于CTF中的Crypto，Misc...

内置目前主流密码（包括但不限于维吉利亚密码，凯撒密码，栅栏密码······）

用户可自主编写插件，但仅支持Python编写插件。编写方法也极为简单。

该项目一直在增强，这一次的重置只保留了部分核心代码，而将UI及优化代码重构，使这个框架支持更多功能。

项目地址：[https://github.com/0Chencc/CTFCrackTools](https://github.com/0Chencc/CTFCrackTools)

下载编译好的版本：https://github.com/0Chencc/CTFCrackTools/releases/

## 多套外观提供使用

本框架支持多套外观使用，将Setting.json中的Theme改为1,2,3分别对应三套主题，什么都不填，或者随便填。都会使用默认主题，为第4套主题。

注意，代码为1的主题，仅支持JDK8及以下JDK版本。不支持JDK9和JDK10。


## 插件编写

```Python
#-*- coding:utf-8 -*-
'''
{
  title:程序标题
  type:程序类型
  author:作者昵称
  dialog:变量
  detail:插件详情
}
'''
def main(a):
    return a
```

现在来具体讲下这些插件的用法，具体应该将下框架的调用方法。

**type：**为什么需要写插件类型呢，我其实有个野心。是打算尽可能的把能遇到的题目类型的解密方式都写进去，比如pwn这些。

**dialog：**这个呢，其实我考虑到了有些解密方式需要多个密钥。故此设计了这个，如果声明了多个密钥，则程序会弹出多个输入框。

**main：**本工具插件调用十分简单，但是限制就是，必须传入数据。

**因为工具调用其实就是通过def mian(a)传入数据然后获取return的数据。**

```Python
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
```

ciphertext是输入框的内容，直接导入的，无需管。

代码的架构是这样的话，框架就可以自行读取插件信息，然后会弹一个窗口请输入key。

如图：![mark](/img/plugin.gif)

```Python
def vigenereDecrypto(ciphertext,key)
```

ciphertext即是输入的内容，key是由弹窗出来由用户填写的。

