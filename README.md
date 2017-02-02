# README 语言/README Language
[中文](https://github.com/0Linchen/CTFCrackTools/blob/master/README.md)
<br/>
[English](https://github.com/0Linchen/CTFCrackTools/blob/master/README_en.md)
# 中国国内首个CTF工具框架
应该是国内首个CTF工具框架。希望有朋友共同维护<br/>
已经编译完成的包：[点击此处即可下载](https://github.com/0Linchen/CTFCrackTools/raw/master/CTFtools.zip)<br/>
[直接跳到开发文档](#python插件开发文档)<br/>
# CTFCrack工具说明
本工具由米斯特安全团队开发<br/>
集成摩斯电码，凯撒密码，栅栏密码，Rot13密码以及各种编码互换等CTF中常见密码加解<br/>
旨在于帮助CTFer攻克CTF中crypto类、Image、zip难关<br/>
本程序支持Python插件，允许使用者自建插件，可直接将py脚本放进Plugin目录中<br/>
程序运行时将自动遍历Plugin目录中的py脚本<br/>
每次程序打开时第一次调用脚本时，会稍卡，因为在加载调用py的插件。大概2秒<br/>
须知：OS目录为程序自带插件，勿删。<br/>
删除了将调用不了某些功能，误删的朋友可到github上下载<br/>
## 使用须知
git上的是源码，需要下载后导入javaIDE编译<br/>
推荐Eclipse导入编译。
# 附上程序截图
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/1.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/2.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/3.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/4.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/5.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/6.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/7.png)
# Python插件开发文档
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/8.png)<br/>
图中是一个我用来debug的程序的插件。也是插件样式。<br/>
我想保护开发者的版权，所以会要求开发者在autor上填写自己的ID。<br/>
因为程序整体都是utf-8编码，所以插件的要求也应该是utf-8<br/>
在声明之后，延续Java的花括号写法<br/>
title:（标题）<br/>
type:（针对类型） Crypto对应crypto Image对应image Zip对应zip<br/>
author：（作者ID）<br/>
detail：（程序详情）<br/>
用}结束<br/>
在Python中def run(String)一个方法，样式：<br/>
```Python
def run(string)
    return string
 ```
因为程序会传入字符，所以return的也应该是String类型<br/>
Image和Zip的，是通过程序传入文件路径，然后再让插件crack后返回crack之后的文件路径。也就是说，尽可能生成在比较容易查找的目录。<br/>
Crypto则是返回Crack之后的字符串。也同样是String类型<br/>
# 鸣谢：
米斯特安全团队：我擦咧什么鬼，z13，Mrlyn<br/>
网友：Void.<br/>
# 末：
“好风凭借力，送我上青云”<br/>
希望能成为你们的好风，早日助你们上青云。
