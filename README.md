# CTFcrypto类工具说明
本工具由米斯特安全团队开发<br/>
集成摩斯电码，凯撒密码，栅栏密码，Rot13密码以及各种编码互换等CTF中常见密码加解<br/>
旨在于帮助CTFer攻克CTFcrypto类难关<br/>
本程序支持Python插件，允许使用者自建插件，可直接将py脚本放进Plugin目录中<br/>
程序运行时将自动遍历Plugin目录中的py脚本<br/>
每次程序打开时第一次调用脚本时，会稍卡，因为在加载调用py的插件。大概2秒<br/>
须知：OS目录为程序自带插件，勿删。<br/>
删除了将调用不了某些功能，误删的朋友可到github上下载<br/>
# 附上程序截图
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/1.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/2.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/3.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/4.png)
# Python插件开发文档
建立xxx.py文件<br/>
定义方法<br/>
def run(data):<br/>
return 返回值<br/>
须知：程序传入数据的方法是String类型，故此数字类型暂不支持<br/>
方法名必须为run，否则调用失败<br/>
需要数字类型的朋友可自行fork分支 然后修改代码<br/>
或者联系我QQ：627437686<br/>
# 鸣谢：
米斯特安全团队：我擦咧什么鬼，z13，Mrlyn<br/>
网友：Void.<br/>
