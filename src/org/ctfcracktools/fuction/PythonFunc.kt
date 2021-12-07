package org.ctfcracktools.fuction

import org.ctfcracktools.json.SettingJson
import org.python.core.*
import org.python.util.PythonInterpreter
import java.util.*


class PythonFunc {
    lateinit var interpreter:PythonInterpreter

    /**
     * 初始化
     */
    init {
        jythonLoad()
    }

    /**
     * 加载jython
     */
    private fun jythonLoad(){
        val props = Properties()
        val setting = SettingJson().parseJson()
        props["python.home"] = setting["jython"]
        props["python.console.encoding"] = "utf-8"
        props["python.security.respectJavaAccessibility"] = "false"
        props["python.import.site"] = "false"
        val sysProps = System.getProperties()
        PythonInterpreter.initialize(sysProps,props, arrayOfNulls(0))
        val sysS = Py.getSystemState()
        sysS.path.add(System.getProperty("user.dir") + "")
        interpreter = PythonInterpreter()
    }

    /**
     * 加载py脚本
     * @param file 文件名(含目录)
     */
    fun loadFile(file:String)= interpreter.execfile(file)

    /**
     * 加载要调用的函数
     * @param interpreter PythonInterpreter
     * @param funcName 函数名
     */
    fun loadPythonFunc(interpreter: PythonInterpreter, funcName: String): PyFunction = interpreter[funcName, PyFunction::class.java]

    /**
     * 执行python脚本（无参数）
     * @param function 配合loadPythonFunc将加载好文件目录、函数的解析成函数形式传入
     */
    fun execFunc(function:PyFunction):Any?{
        var pyObject:PyObject? = null
        try{
            pyObject = function.__call__()
        }catch (e: PyException){
            e.printStackTrace()
        }
        return pyObject!!.__tojava__(Any::class.java)
    }

    /**
     * 执行python脚本（含参数）
     * @param function 配合loadPythonFunc将加载好文件目录、函数的解析成函数形式传入
     * @param values 多参数
     */
    fun execFuncOfArr(function: PyFunction,vararg values: String?): Any? {
        val strings = arrayOfNulls<PyString>(values.size)
        for (i in strings.indices) {
            strings[i] = Py.newString(values[i])
        }
        var pyObject: PyObject? = null
        try {
            pyObject = function.__call__(strings)
        } catch (e: PyException) {
            e.printStackTrace()
        }
        return pyObject!!.__tojava__(Any::class.java)
    }

    /**
     * 获取作者信息
     * @param file 文件地址
     * @return Map<String,Object> 返回一个含有作者信息的map
     */
    fun getAuthorInfo(file:String):Map<String,Any>  {
        loadFile(file)
        return execFunc(loadPythonFunc(interpreter,"author_info")) as Map<String, Any>}
    }