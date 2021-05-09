//美化json
class JsonFormatTool {
    /**
     * 返回格式化JSON字符串。
     *
     * @param json 未格式化的JSON字符串。
     * @return 格式化的JSON字符串。
     */
    fun formatJson(json: String): String {
        val result=StringBuffer()
        val length=json.length
        var number=0
        var key: Char
        for (i in 0 until length) {
            key=json[i]
            if(key=='[' || key=='{') {
                if(i-1 > 0 && json[i-1]==':') {
                    result.append('\n')
                    result.append(indent(number))
                }
                result.append(key)
                result.append('\n')
                number++
                result.append(indent(number))
                continue
            }
            if(key==']' || key=='}') {
                result.append('\n')
                number--
                result.append(indent(number))
                result.append(key)
                if(i+1 < length && json[i+1]!=',') {
                    result.append('\n')
                }
                continue
            }
            if(key==',') {
                result.append(key)
                result.append('\n')
                result.append(indent(number))
                continue
            }
            result.append(key)
        }
        return result.toString()
    }
    /**
     * 返回指定次数的缩进字符串。每一次缩进三个空格，即SPACE。
     *
     * @param number 缩进次数。
     * @return 指定缩进次数的字符串。
     */
    private fun indent(number: Int): String {
        val result=StringBuffer()
        for (i in 0 until number) {
            result.append(SPACE)
        }
        return result.toString()
    }
    companion object {
        /**
         * 单位缩进字符串。
         */
        private val SPACE="   "
    }
}