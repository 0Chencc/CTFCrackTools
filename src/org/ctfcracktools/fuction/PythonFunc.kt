package org.ctfcracktools.function

import org.ctfcracktools.json.SettingJson
import org.python.core.*
import org.python.util.PythonInterpreter
import java.util.*

class PythonFunc {
    private lateinit var interpreter: PythonInterpreter

    /**
     * 初始化Python解释器。
     */
    init {
        try {
            loadJython()
        } catch (e: Exception) {
            println("Jython加载失败")
            e.printStackTrace()
        }
    }

    /**
     * 加载Jython并配置属性。
     */
    private fun loadJython() {
        val props = Properties()
        val setting = SettingJson().parseJson()
        props["python.home"] = setting["jython"]
        props["python.console.encoding"] = "utf-8"
        props["python.security.respectJavaAccessibility"] = "false"
        props["python.import.site"] = "false"
        val sysProps = System.getProperties()
        PythonInterpreter.initialize(sysProps, props, arrayOfNulls(0))
        val sysState = Py.getSystemState()
        sysState.path.add(System.getProperty("user.dir"))
        interpreter = PythonInterpreter()
    }

    /**
     * 加载一个Python文件。
     * @param file 文件名（包括目录）。
     */
    fun loadFile(file: String) = interpreter.execfile(file)

    /**
     * 根据名称加载Python函数。
     * @param funcName 函数名。
     * @return 加载的Python函数。
     */
    fun loadPythonFunc(funcName: String): PyFunction = interpreter[funcName, PyFunction::class.java]

    /**
     * 执行不带参数的Python函数。
     * @param function 要执行的函数。
     * @return 函数调用的结果。
     */
    fun execFunc(function: PyFunction): Any? {
        var pyObject: PyObject? = null
        try {
            pyObject = function.__call__()
        } catch (e: PyException) {
            e.printStackTrace()
        }
        return pyObject?.__tojava__(Any::class.java)
    }

    /**
     * 执行带参数的Python函数。
     * @param function 要执行的函数。
     * @param values 要传递给函数的参数。
     * @return 函数调用的结果。
     */
    fun execFuncOfArr(function: PyFunction, vararg values: String?): Any? {
        val strings = Array(values.size) { i -> Py.newString(values[i]) }
        var pyObject: PyObject? = null
        try {
            pyObject = function.__call__(*strings)
        } catch (e: PyException) {
            e.printStackTrace()
        }
        return pyObject?.__tojava__(Any::class.java)
    }

    /**
     * 从Python脚本中获取作者信息。
     * @param file 文件地址。
     * @return 包含作者信息的Map。
     */
    fun getAuthorInfo(file: String): Map<String, Any> {
        loadFile(file)
        return execFunc(loadPythonFunc("author_info")) as Map<String, Any>
    }
}
