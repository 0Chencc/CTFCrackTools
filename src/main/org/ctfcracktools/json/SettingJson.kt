package org.ctfcracktools.json

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.*

class SettingJson {
    private var settingFile = File("ctfracktools_setting.json")
    init {
        if(!isJson()){
            val initSetting = mapOf<String,String>("Jython" to "")
            settingFile.createNewFile()
            writeJson(initSetting)
        }
    }
    fun parseJson():Map<String,String>{
        val settingReader = BufferedReader(FileReader(settingFile))
        return Gson().fromJson(settingReader, object : TypeToken<Map<String, String>>() {}.type)
    }
    fun writeJson(setting:Map<String,String>){
        val gson = GsonBuilder().setPrettyPrinting().create()
        val writer = BufferedWriter(FileWriter(settingFile))
        writer.write(gson.toJson(setting))
        writer.flush()
    }
    fun isJson():Boolean = settingFile.isFile && settingFile.exists()
}