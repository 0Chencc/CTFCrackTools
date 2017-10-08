# CTFcrackTools-V3
>[![Build Status](https://travis-ci.org/0Chencc/CTFCrackTools.svg?branch=master)](https://travis-ci.org/0Chencc/CTFCrackTools)
>[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-blue.svg)](https://raw.githubusercontent.com/0Chencc/CTFCrackTools/master/doc/LICENSE)
>[![language](https://img.shields.io/badge/language-java-orange.svg)](https://github.com/0Chencc/CTFCrackTools/)
>
> CTFcrackTools重置版
>
> 作者：米斯特安全-林晨、摇摆、奶权
>
> 米斯特安全团队首页：[http://www.hi-ourlife.com/](http://www.hi-ourlife.com/)
>
> 部分插件来源：希望团队-nMask
## 第二版
应老用户要求，将继续更新V2版本。以下是项目地址：

[https://github.com/0Chencc/CTFCrackTools-V2](https://github.com/0Chencc/CTFCrackTools-V2)

## 框架介绍

这大概是国内首个应用于CTF的工具框架。

可以被应用于CTF中的Crypto，Misc...

内置目前主流密码（包括但不限于维吉利亚密码，凯撒密码，栅栏密码······）

用户可自主编写插件，但仅支持Python编写插件。编写方法也极为简单。

该项目一直在增强，这一次的重置只保留了部分核心代码，而将UI及优化代码重构，使这个框架支持更多功能。

项目地址：[https://github.com/0Chencc/CTFCrackTools](https://github.com/0Chencc/CTFCrackTools)

下载编译好的版本：https://github.com/0Chencc/CTFCrackTools/releases/

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

> 编码类型当然是utf-8啦
>
> Type:Crypto是一个硬性要求，因为我目前只写了Crypto的类，我打算在后期加上压缩包，图片的分类出来，慢慢完善。
>
> main的方法中，至少有一个变量，至多有四个变量。
>
> 除了第一个变量以外的，都应该在Dialog后标明。
>
> Example：我们团队的奶权写了一个维基利亚密码的插件

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

这样写的话，框架就可以自行读取插件信息，然后会弹一个窗口请输入key。而ciphertext则是直接传入。

如图：![mark](/img/1.png)

![mark](/img/2.png)

![mark](/img/3.png)

```Python
def vigenereDecrypto(ciphertext,key)
```

ciphertext即是输入的内容，key是由弹窗出来由用户填写的。

## 界面介绍

![mark](/img/use.gif)
