# 中国国内首个CTFcrack框架
不出意外，应该是国内首个CTFcrack框架。希望有朋友共同维护<br/>
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
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/8.png)
建立xxx.py文件<br/>
用{<br/>
title： 则是插件标题<br/>
type:   破解类型（如Crypto，则写crypro 如压缩包类 就是zip 如果是图片，则是image）<br/>
autor:  是作者ID<br/>
detail: 写插件详情，可以写上使用方法等等<br/>
}
定义方法<br/>
def run(data):<br/>
return 返回值<br/>
如果是Image类型，就需要return crack后的图片地址<br/>
如果是Zip类型，则return crack后的zip地址<br/>
软件会自己跑<br/>
须知：程序传入数据的方法是String类型(可在python中转换类型)<br/>
方法名必须为run，否则调用失败<br/>
需要数字类型的朋友可自行fork分支 然后修改代码<br/>
或者联系我QQ：627437686<br/>
# 鸣谢：
米斯特安全团队：我擦咧什么鬼，z13，Mrlyn<br/>
网友：Void.<br/>
