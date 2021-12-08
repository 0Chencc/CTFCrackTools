package org.ctfcracktools.json

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.*
import kotlin.collections.ArrayList

class PluginsJson {
    private var jsonFile = File("ctfcracktools_plugins.json")

    /**
     * 初始化
     */
    init{
        if(!isJson()){
            val initPlugins = arrayListOf<Map<String,Any>>()
            jsonFile.createNewFile()
            writeJson(initPlugins)
        }
    }

    /**
     * 解析json文件
     * @return 返回一个Map<String,Object>的ArrayList插件列表
     */
    fun parseJson(): ArrayList<Map<String, Any>> {
        val pluginsReader = BufferedReader(FileReader(jsonFile))
        return Gson().fromJson(pluginsReader, object : TypeToken<ArrayList<Map<String, Any>>>() {}.type)
    }

    /**
     * 根据name去json文件中进行搜索，返回第一个
     * @param name String 插件名称
     */
    fun search(name:String):Map<String,Any>{
        val plugins = parseJson()
        var plugin:Map<String,Any> = HashMap()
        plugins.forEach {
            if(it["name"].toString() == name){
                plugin = it
            }
        }
        return plugin
    }

    /**
     * 删除插件
     * @param plugin Map<String,Object> 传入一个plugin的信息，进行删除
     */
    fun removePlugin(plugin:Map<String,Any>){
        val plugins = parseJson()
        plugins.remove(plugin)
        writeJson(plugins)
    }

    /**写入配置文件
     * @param plugins ArrayList<Map<String,Object>> 插件别表
     */
    fun writeJson(plugins:ArrayList<Map<String,Any>>){
        val gson = GsonBuilder().setPrettyPrinting().create()
        val writer = BufferedWriter(FileWriter(jsonFile))
        writer.write(gson.toJson(plugins))
        writer.flush()
    }

    /**
     * 判断是否为配置文件
     * @return Boolean
     */
    fun isJson():Boolean = jsonFile.isFile && jsonFile.exists()
}