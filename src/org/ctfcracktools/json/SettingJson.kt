package org.ctfcracktools.json

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import org.ctfcracktools.Config
import java.io.*

class SettingJson {
    init {
        if(!isJson()){
            val initSetting = mapOf("jython" to "")
            Config.SETTING_FILE.createNewFile()
            writeJson(initSetting)
        }
    }

    /**
     * 返回一个储存配置信息的Map
     * @return Map<String,String>
     */
    fun parseJson():Map<String,String>{
        val settingReader = BufferedReader(FileReader(Config.SETTING_FILE))
        return Gson().fromJson(settingReader, object : TypeToken<Map<String, String>>() {}.type)
            ?: return mapOf(pair = "jython" to "")
    }

    /**
     * 将配置信息写入json文件
     * @param Setting String 配置信息
     */
    fun writeJson(setting:Map<String,String>){
        val gson = GsonBuilder().setPrettyPrinting().create()
        val writer = BufferedWriter(FileWriter(Config.SETTING_FILE))
        writer.write(gson.toJson(setting))
        writer.flush()
    }
    fun isJson():Boolean = Config.SETTING_FILE.isFile && Config.SETTING_FILE.exists()
}