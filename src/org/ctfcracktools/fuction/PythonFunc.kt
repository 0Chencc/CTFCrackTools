package org.ctfcracktools.fuction

import org.ctfcracktools.json.SettingJson
import org.python.core.*
import org.python.util.PythonInterpreter
import java.util.*


class PythonFunc {
    lateinit var interpreter:PythonInterpreter
    init {
        jythonLoad()
    }
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
    fun loadFile(file:String)= interpreter.execfile(file)
    fun loadPythonFunc(interpreter: PythonInterpreter, funcName: String): PyFunction = interpreter[funcName, PyFunction::class.java]
    fun execFunc(function:PyFunction):Any?{
        var pyObject:PyObject? = null
        try{
            pyObject = function.__call__()
        }catch (e: PyException){
            e.printStackTrace()
        }
        return pyObject!!.__tojava__(Any::class.java)
    }
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
    fun getAuthorInfo(file:String):Map<String,Any>  {
        loadFile(file)
        return execFunc(loadPythonFunc(interpreter,"author_info")) as Map<String, Any>}
    }