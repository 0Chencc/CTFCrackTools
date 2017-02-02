# README 语言/README Language
[中文](https://github.com/0Linchen/CTFCrackTools/blob/master/README.md)
<br/>
[English](https://github.com/0Linchen/CTFCrackTools/blob/master/README_en.md)
# China's first CTFtools framework
Should be the first CTFtools framework. Hope that a friend to maintain together<br/>
Compiled packages: [Download here] (https://github.com/0Linchen/CTFCrackTools/raw/master/CTFtools.zip)
[Jump directly to the development documentation] (# python plugin development documentation)
# CTFCrack tool description
This tool was developed by the Mist security team(MSEC Team) <br/>
Integrated Moss code, Caesar password, fence password, Rot13 password and a variety of code-switching and other common cryptography CTF solution <br/>
Designed to help CTFer capture CTF crypto class, Image, zip difficult
This program supports Python plug-ins, allowing users to self-built plug-ins, py scripts can be directly into the Plugin directory <br/>
The py script in the Plugin directory is automatically traversed while the program is running <br/>
The first time the script is called each time the program is opened, it will be slightly loaded because the plugin that calls py is loaded. About 2 seconds <br/>
Note: OS directory for the program comes with plug-ins, do not delete. <br/> <br/> 
Deleted will not be able to call some functions, accidentally deleted friends can be downloaded to github <br/>
## Terms and Conditions
Git is the source code, the need to download into javaIDE compiler
Recommended Eclipse import compilation.
# Attach a screenshot of the program
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/1.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/2.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/3.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/4.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/5.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/6.png)
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/7.png)
# Python development documentation
![image](https://github.com/0Linchen/CTFcryptoCrack/blob/master/images-folder/8.png)<br/>
The figure is a program I used to debug the plug-in. Also plug-in style. <br/> <br/>
I want to protect the developer's copyright, so developers will be asked to fill in the autor own ID. <br/> <br/>
Since the whole program is utf-8 encoding, so the plug-in requirements should be utf-8 <br/>
After the declaration, the Java braces are continued <br/>
Title: (title) <br/>
Type: (for type) Crypto corresponds to crypto Image corresponds to image Zip corresponds to zip <br/>
Author: (author ID) <br/>
Detail: (program details) <br/>
End with}<br/>
Def run (String) A method in Python, style:<br/>
```Python
Def run (string)
    Return string
```
Because the program will pass characters, so the return should also be a String type <br/>
Image and Zip, is passed through the program file path, and then let the plug after the crack crack to return after the file path. In other words, as far as possible in the relatively easy to find directory. <br/> <br/>
Crypto is the string that returns Crack. Is also of the String type <br/>
# Acknowledgments:
Mist security team(MSEC Team): 我擦咧什么鬼, z13, Mrlyn<br/>
User: Void<br/>
# At the end:
"Good wind with force, send me on the Albatron."<br/>
Hoping to become your good wind, as soon as possible to help you on Albatron.
