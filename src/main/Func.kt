import org.apache.commons.codec.binary.Base32
import org.apache.commons.codec.binary.Base64.*
import java.net.URLDecoder
import java.net.URLEncoder
import java.util.*
import java.util.regex.Matcher
import java.util.regex.Pattern
/**
 * @author 林晨0chencc
 * @since 2017/12/2
 * @version 1.0.0
 */
class Func{
    fun Fence(input: String):String {
        val str:Array<String?> = arrayOfNulls<String>(1024)
        val x = IntArray(1024)
        val result = StringBuffer()
        var a = 0
        var nums = 0
        if (input.length!=1&&input.length!=2) {
            (2 until input.length).forEach { i ->
                if (input.length % i == 0) {
                    x[a] = i
                    a++
                }
            }
        }
        if(a!=0) {
            (0 until a).forEach { i ->
                result.append("${i + 1}：")
                (0 until input.length / x[i]).forEach { j ->
                    str[nums] = input.substring(0 + (x[i] * j), x[i] + (x[i] * j))
                    nums++
                }
                (0 until str[0]!!.length).forEach { ji ->
                    (0 until nums).forEach { s -> result.append(str[s]!!.substring(ji,ji+1)) }
                }
                nums =0
                result.append("\n")
            }
        }else{
            val newstrlenth:Int = input.replace(" ","").length
            if (newstrlenth !=1 && newstrlenth !=2){
                (2..newstrlenth-1).forEach { i ->
                    if (newstrlenth%i==0){
                        x[a]=i
                        a++
                    }
                }
            }
            if (a !== 0) {
                (0 until a).forEach { it -> result.append(" " + x[it]) }
                (0 until a).forEach { i ->
                    result.append("${i+1}：")
                    (0 until newstrlenth / x[i]).forEach { j ->
                        str[nums] = input.substring(0 + x[i] * j, x[i] + x[i] * j)
                        nums++
                    }
                    (0 until str[0]!!.length).forEach { j ->
                        (0 until nums).forEach { result.append(str[it]!!.substring(j, j + 1)) }
                    }
                    nums = 0
                    result.append('\n')
                }
            }
        }
        return result.toString()
    }//栅栏密码
    fun Caesar(input:String):String{
        val word:CharArray=input.toCharArray()
        val result = StringBuffer()
        (0 until 26).forEach {
            (0 until word.size).forEach { j ->
                if (word[j].isUpperCase()){
                    if(word[j]=='Z') word[j]='A' else word[j] = (word[j].toInt() + 1).toChar()
                }else if(word[j].isLowerCase()){
                    if(word[j]=='z') word[j]='a' else word[j]=(word[j].toInt()+1).toChar()
                }
            }
            result.append(word+'\n')
        }
        return result.toString()
    }//凯撒密码
    fun VigenereEnCode(input:CharArray,key:CharArray): String {
        var i:Int = 0
        var j:Int = 0
        var q:Int = 0
        var k:Int
        var m:Int
        return StringBuilder()
                .let{
                    result ->
                    while (i<input.size) {
                        when {
                            input[i].isUpperCase() -> {
                                j = q%key.size
                                k = UpperCase.indexOf(key[j].toUpperCase())
                                m = UpperCase.indexOf(input[i])
                                result.append(UpperCase[(m+k)%26])
                                q++
                            }
                            input[i].isLowerCase() -> {
                                j = q%key.size
                                k = LowerCase.indexOf(key[j].toLowerCase())
                                m = LowerCase.indexOf(input[i])
                                result.append(LowerCase[(m+k)%26])
                                q++
                            }
                            else -> result.append(input[i])
                        }
                        i++
                    }
                    result
                }
                .toString()
    }
    fun VigenereDeCode(input:CharArray,key: CharArray):String{
        var i:Int = 0
        var j:Int = 0
        var q:Int = 0
        var k:Int
        var m:Int
        return StringBuilder()
                .let{
                    result ->
                    while (i<input.size) {
                        when {
                            input[i].isUpperCase() -> {
                                j = q%key.size
                                k = UpperCase.indexOf(key[j].toUpperCase())
                                m = UpperCase.indexOf(input[i])
                                if(m<k)
                                    m+=26
                                result.append(UpperCase[m-k])
                                q++
                            }
                            input[i].isLowerCase() -> {
                                j = q%key.size
                                k = LowerCase.indexOf(key[j].toLowerCase())
                                m = LowerCase.indexOf(input[i])
                                if(m<k)
                                    m+=26
                                result.append(LowerCase[m-k])
                                q++
                            }
                            else -> result.append(input[i])
                        }
                        i++
                    }
                    result
                }
                .toString()
    }
    fun PigCode(input:String):String{
        val result = StringBuffer()
        val keymap= mapOf('A' to 'J','B' to 'K','C' to 'L','D' to 'M',
                'E' to 'N','F' to 'O','G' to 'P','H' to 'Q','I' to 'R','J' to 'A','K' to 'B','L' to 'C',
                'M' to 'D','N' to 'E','O' to 'F','P' to 'G','Q' to 'H','R' to 'I','S' to 'W','T' to 'X',
                'U' to 'Y','V' to 'Z','W' to 'S','X' to 'T')
        val word = input.toCharArray()
        for (i in 0 until word.size){
            if (word[i].isUpperCase()){
                result.append(keymap.get(word[i])!!)
            }else if(word[i].isLowerCase()){
                result.append(keymap.get(word[i].toUpperCase())!!.toLowerCase())
            }else{
                result.append(word[i])
            }
        }
        return result.toString()
    }//猪圈密码
    fun Rot13(input:String):String{
        var word = input.toCharArray()
        val result = StringBuffer()
        for (i in 0 until word.size){
            when {
                word[i] in 'a'..'m' -> word[i]=(word[i].toInt()+13).toChar()
                word[i] in 'A'..'M' -> word[i]=(word[i].toInt()+13).toChar()
                word[i] in 'n'..'z' -> word[i]=(word[i].toInt()-13).toChar()
                word[i] in 'N'..'Z' -> word[i]=(word[i].toInt()-13).toChar()
            }
            result.append(word[i])
        }
        return result.toString()
    }//Rot13
    fun BaconCodeEncode(input:String):String{
        val keymap = mapOf("A" to "aaaaa","B" to "aaaab","C" to "aaaba",
                "D" to "aaabb","E" to "aabaa","F" to "aabab","G" to "aabba","H" to "aabbb","I" to "abaaa",
                "J" to "abaab","K" to "ababa","L" to "ababb","M" to "abbaa","N" to "abbab","O" to "abbba",
                "P" to "abbbb","Q" to "baaaa","R" to "baaab","S" to "baaba","T" to "baabb","U" to "babaa",
                "V" to "babab","W" to "babba","X" to "babbb","Y" to "bbaaa","Z" to "bbaab","a" to "AAAAA",
                "b" to "AAAAB","c" to "AAABA","d" to "AAABB","e" to "AABAA","f" to "AABAB","g" to "AABBA",
                "h" to "AABBB","i" to "ABAAA","j" to "ABAAB","k" to "ABABA","l" to "ABABB","m" to "ABBAA",
                "n" to "ABBAB","o" to "ABBBA","p" to  "ABBBB","q" to "BAAAA",
                "r" to "BAAAB","s" to "BAABA","t" to "BAABB","u" to "BABAA","v" to "BABAB","w" to "BABBA",
                "x" to "BABBB","y" to "BBAAA","z" to "BBAAB")
        return StringBuilder()
                .let{
                    result ->
                    if(is26word(input)) {
                        SplitNum(input,1).forEach {result.append(keymap[it])}
                    }else{
                        result.append("有字符不属于26字母其中")
                    }
                    result
                }
                .toString()
    }//培根密码加密
    fun BaconCodeDecode(input: String):String{
        val keymap = mapOf("aaaaa" to 'A',"aaaab" to 'B',"aaaba" to 'C',
                "aaabb" to 'D',"aabaa" to 'E',"aabab" to 'F',"aabba" to 'G',"aabbb" to 'H',"abaaa" to 'I',
                "abaab" to 'J',"ababa" to 'K',"ababb" to 'L',"abbaa" to 'M',"abbab" to 'N',"abbba" to 'O',
                "abbbb" to 'P',"baaaa" to 'Q',"baaab" to 'R',"baaba" to 'S',"baabb" to 'T',"babaa" to 'U',
                "babab" to 'V',"babba" to 'W',"babbb" to 'X',"bbaaa" to 'Y',"bbaab" to 'Z',//UpperCase大写字符
                "AAAAA" to 'a',"AAAAB" to 'b',"AAABA" to 'c',"AAABB" to 'd',"AABAA" to 'e',"AABAB" to 'f',
                "AABBA" to 'g',"AABBB" to 'h',"ABAAA" to 'i',"ABAAB" to 'j',"ABABA" to 'k',
                "ABABB" to 'l',"ABBAA" to 'm',"ABBAB" to 'n',"ABBBA" to 'o', "ABBBB" to 'p',"BAAAA" to 'q',
                "BAAAB" to 'r',"BAABA" to 's',"BAABB" to 't',"BABAA" to 'u',"BABAB" to 'v',"BABBA" to 'w',
                "BABBB" to 'x',"BBAAA" to 'y',"BBAAB" to 'z'
        )
        return StringBuilder()
                .let{
                    result ->
                    var inputnew:String = ""
                    if(isBacon(input)){
                        inputnew = input.replace(" ","")
                        SplitNum(inputnew,5,"[ab]{5}").forEach { result.append(keymap[it]) }
                    }else{
                        result.append("并非是培根密码")
                    }
                    result
                }
                .toString()
    }//培根密码解密
    fun Base64de(input: String):String = String(decodeBase64(input))//Base64解码
    fun Base64en(input: String):String = encodeBase64String(input.toByteArray())//Base64编码
    fun Base32de(input:String):String = String(Base32().decode(input))//Base32解码
    fun Base32en(input:String):String = Base32().encodeAsString(input.toByteArray())//Base32编码
    fun HextoString(input:String):String{
        return StringBuilder()
                .let{
                    result ->
                    (0 until input.length-1 step 2)
                            .map{ input.substring(it, it+2) }
                            .map { Integer.parseInt(it,16) }
                            .forEach { result.append(it.toChar()) }
                    result
                }
                .toString()
    }//16进制转字符串
    fun StringtoHex(input:String):String{
        return StringBuilder()
                .let{
                    result ->
                    input.toCharArray().forEach {result.append(Integer.toHexString(it.toInt())) }
                    result
                }
                .toString()
    }//字符串转16进制
    fun MorseEncode(input: String):String {
        return StringBuilder()
                .let{
                    result ->
                    input.toLowerCase().toCharArray().forEach {
                        when {
                            isChar(it) -> result.append(morseCharacters[(it - 'a')]+" ")
                            isDigit(it) -> result.append(morseDigits[(it - '0')]+" ")
                        }
                    }
                    result
                }
                .toString()
    }//摩斯密码加密
    fun MorseDecode(input:String):String{
        initMorseTable()
        val morse=format(input)
        val st=StringTokenizer(morse)
        val result=StringBuilder(morse.length / 2)
        while (st.hasMoreTokens()) {
            result.append(htMorse[st.nextToken()])
        }
        return result.toString()
    }//摩斯密码解码
    fun UrlEncoder(input: String):String = URLEncoder.encode(input,"utf-8").replace("+","%20")//Url编码加密
    fun URLDecoder(input: String):String = URLDecoder.decode(input,"utf-8")//Url编码解密
    fun UnicodeEncode(input: String):String{
        return StringBuilder()
                .let {
                    result ->
                    input.toCharArray().forEach {result.append("\\u"+Integer.toHexString(it.toInt())) }
                    result
                }
                .toString()
    }//Unicode编码
    fun UnicodeDecode(input: String):String{
        return StringBuilder()
                .let{
                    result ->
                    val hex=input.split("\\u")
                    (1 until hex.size)
                            .map { Integer.parseInt(hex[it], 16) }
                            .forEach { result.append(it.toChar()) }
                    result
                }
                .toString()
    }//Unicode解码
    fun UnicodeToAscii(input:String):String{
        return StringBuilder()
                .let{
                    result ->
                    val pout = Pattern.compile("\\&\\#(\\d+)").matcher(input)
                    while (pout.find()){ result.append(Integer.valueOf(pout.group(1)).toInt().toChar()) }
                    result
                }
                .toString()
    }//Unicode编码转换为Ascii编码
    fun AsciiToUnicode(input: String):String{
        return StringBuilder()
                .let {
                    result ->
                    input.toCharArray().forEach { result.append("&#"+it.toInt()+";")}
                    result
                }
                .toString()
    }
    fun reverse(input:String):String{
        val result = StringBuilder()
        val tmp = input.toCharArray()
        var a=tmp.size-1
        while (a > -1) {
            result.append(tmp[a])
            a-=1
        }
        return result.toString()
    }//字符翻转
/*    fun HillCodeEncode(input:String,key:String):String{
        val keymatrix:CharArray = key.split(" ") as CharArray
        var tmp[]:<String?>Array
        when{
            keymatrix.size/4 == 0 ->
                0 until keymatrix.size%4.forEach{

        }

        }
        return StringBuffer()
                .let {
                    result->

                }
                .toString()
    }*/
    /* 调用Python的插件 */

    /* 内置方法/内置常量 */
    val UpperCase:String ="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    val LowerCase:String = "abcdefghijklmnopqrstuvwxyz"
    val SplitString = {//多次切割字符串
        input:String ->
        val tmp = input.split(",")
        val result = StringBuilder()
        tmp.forEach{
            val tmp_1 = it.split(" to ")
            result.append(tmp_1[1]+" to "+tmp_1[0]+",")
        }
        result.toString()
    }
/*    val SplitNum = {//写一个隔字符分割的方法23333...
        input: String, Num: Int ->
        val str: Array<String?> = arrayOfNulls<String>(input.length / Num)
        (1..input.length / Num).forEach { i -> str.set(i-1, input.substring(i * Num-Num, i * Num)) }
        str
    }*/
    /*  SpiltNum,第一个参数是字符串，第二个字符串按几个为一组进行分割，第三个参数是正则规则
    * */
    fun SplitNum(input:String,Num:Int):Array<String?>{
        val str:Array<String?> = arrayOfNulls<String>(input.length/Num)
        (1..input.length/Num).forEach { i->str.set(i-1,input.substring(i*Num-Num,i*Num)) }
        return str
    }
    fun SplitNum(input:String,Num:Int,p:String):Array<String?>{
        val r:Pattern = Pattern.compile(p)
        val m: Matcher = r.matcher(input)
        var input_m = ""
        var a = true
        while (a){
            if(!m.find()) a=false else input_m += m.group()
        }
        val str:Array<String?> = arrayOfNulls<String>(input_m.length/Num)
        (1..input_m.length/Num).forEach { i->str.set(i-1,input_m.substring(i*Num-Num,i*Num)) }
        return str
    }
    val isBacon = {
        input:String ->
        var tmp:Boolean = false
        input.toCharArray().forEach {
            tmp = (it=='A'||it=='B')||(it == 'a'||it=='b')
        }
        tmp
    }
    val is26word = {
        input:String ->
        var tmp = false
        input.toCharArray().forEach {
            tmp = isChar(it)
        }
        tmp
    }
    var htMorse: Hashtable<String, Char> = Hashtable()
    fun initMorseTable(){
        (0..25).forEach { i -> htMorse.put(morseCharacters[i], Character.valueOf((65+i).toChar())) }
        (0..9).forEach { i -> htMorse.put(morseDigits[i], Character.valueOf((48+i).toChar())) }
    }
    val isChar = {c:Char -> c.isLowerCase()||c.isUpperCase()}
    val isDigit = {c:Char -> (c >='0')&&(c <= '9')}
    /* moresCode */
    val morseCharacters = arrayOf(".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", ".---",
            "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--",
            "--..")
    val morseDigits = arrayOf("-----", ".----", "..---", "...--", "....-", ".....", "-....", "--...",
            "---..", "----.")
    val format = {
        input:String->
        val word = input.toCharArray()
        val result = StringBuilder()
        for(i in 0 .. word.size-1){
            when{
                word[i] == '\n' -> word[i]=' '
                word[i] == '.' -> {
                    result.append(word[i])
                }
                word[i] == '-' -> {
                    result.append(word[i])
                }
                word[i] == ' ' -> {
                    result.append(word[i])
                }
            }
        }
        result.toString()
    }
}

/* Debug*/
    fun main(args: Array<String>) {
    val f=Func()
    println(f.BaconCodeDecode("baaba aabbb abaaa bbaaa aaaaa abbab aaaab aaaaa abaaa baaba  aaaba abbba abbba ababb"))
}
