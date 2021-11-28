package org.ctfcracktools.json

import com.google.gson.Gson
import com.google.gson.GsonBuilder
import com.google.gson.reflect.TypeToken
import java.io.*
import kotlin.collections.ArrayList

class PluginsJson {
    private var jsonFile = File("ctfcracktools_plugins.json")
    init{
        if(!isJson()){
            val initPlugins = arrayListOf<Map<String,Any>>()
            jsonFile.createNewFile()
            writeJson(initPlugins)
        }
    }
    fun parseJson(): ArrayList<Map<String, Any>> {
        val pluginsReader = BufferedReader(FileReader(jsonFile))
        return Gson().fromJson(pluginsReader, object : TypeToken<ArrayList<Map<String, Any>>>() {}.type)
    }
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
    fun removePlugin(plugin:Map<String,Any>){
        val plugins = parseJson()
        plugins.remove(plugin)
        writeJson(plugins)
    }
    fun writeJson(plugins:ArrayList<Map<String,Any>>){
        val gson = GsonBuilder().setPrettyPrinting().create()
        val writer = BufferedWriter(FileWriter(jsonFile))
        writer.write(gson.toJson(plugins))
        writer.flush()
    }
//    fun getDialog(dialog: Any?):ArrayList<*> = dialog as ArrayList<*>
    fun isJson():Boolean = jsonFile.isFile && jsonFile.exists()
}