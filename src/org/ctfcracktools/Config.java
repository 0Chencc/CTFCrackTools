package org.ctfcracktools;

import org.ctfcracktools.fuction.PythonFunc;

import java.io.File;

/**
 * @author linchen
 */
public class Config {
    public final static String VERSION = "4.0.6";
    public final static String SLOGAN = "";
    public final static String ABOUT =
            "Author:0chen(@0chencc)\n" +
            "Twitter:@0chencc\n" +
            "GitHub:https://github.com/0Chencc\n" +
            "Wechat Official Accounts(公众号):XizhouPoetry\n" +
            "Repository Url：https://github.com/0Chencc/CTFCrackTools\n" +
            "米斯特安全团队招CTF选手，有意向联系admin@hi-ourlife.com";
    public final static File PLUGIN_FILE = new File("ctfcracktools_plugins.json");
    public final static File SETTING_FILE = new File("ctfcracktools_setting.json");

    public static PythonFunc pyFunc = new PythonFunc();

}
