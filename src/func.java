import java.io.IOException;
import java.io.UnsupportedEncodingException;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.util.Hashtable;
import java.util.StringTokenizer;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

import org.python.core.PyFunction;
import org.python.core.PyObject;
import org.python.core.PyString;
import org.python.util.PythonInterpreter;

import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;
public interface func {
	public static String Zhalan(String input){//栅栏解码
		String zlstr[]= new String[1024];
		int num = 0;
		StringBuffer jg = new StringBuffer();
		 int x[] = new int[1024];
		 int sl = input.length();
		 int a = 0;
		 int i=0;
		 if (sl!=1&&sl!=2){
			 for (i=2;i<sl;i++) {
				 if ((sl%i)==0){
					 x[a]=i;
					 a = a+1;
				 }
			 }
		 }else{
			 jg.append("用肉眼就能看出来\n");
		 }
		 if (a!=0){
			 jg.append("得到因数(排除1和字符串长度):\n");
			 for(int yi=0;yi<a;yi++){
				 jg.append(" "+x[yi]);
			 }
			 jg.append("\n");
			 jg.append("\n");
			 for(i=0;i<a;i++){
				 jg.append("第"+(i+1)+"栏：");
				 for(int j=0;j<(sl/x[i]);j++){
					 zlstr[num]=(input.substring((0+(x[i]*j)), (x[i]+(x[i]*j))));
					 num++;
				 }
				 int slen = zlstr[0].length();
				 for(int ji = 0;ji<slen;ji++){
					 for(int s=0;s<num;s++){
						 jg.append(zlstr[s].substring(ji, ji+1));
					 }
				 }
				 num = 0;
				 jg.append("\n");
			 }
		 }else{
			 jg.append("解码失败...\n");
			 jg.append("尝试去除字符串中的空格解码\n");
			 sl = input.replace(" ", "").length();
			 jg.append(sl);
			 if (sl!=1&&sl!=2){
				 for (i=2;i<sl;i++) {
					 if ((sl%i)==0){
						 x[a]=i;
						 a = a+1;
					 }
				 }
			 }else{
				 jg.append("用肉眼就能看出来\n");
			 }
			 if (a!=0){
				 jg.append("这串密文(去除空格后)是栅栏密码...\n");
				 jg.append("得到因数(排除1和字符串长度):");
				 for(int yi=0;yi<a;yi++){
					 jg.append(" "+x[yi]);
				 }
				 jg.append("\n");
				 jg.append("\n");
				 jg.append("开始解码...");
				 for(i=0;i<a;i++){
					 jg.append("第"+(i+1)+"栏：");
					 for(int j=0;j<(sl/x[i]);j++){
						 zlstr[num]=(input.substring((0+(x[i]*j)), (x[i]+(x[i]*j))));
						 num++;
					 }
					 int slen = zlstr[0].length();
					 for(int ji = 0;ji<slen;ji++){
						 for(int s=0;s<num;s++){
							 jg.append(zlstr[s].substring(ji, ji+1));
						 }
					 }
					 num = 0;
					 jg.append("\n");
				 }
		 }
	   }
	 return jg.toString();
	 }
	public static String Caesar(String input){//凯撒密码
	    char[] ca = input.toCharArray();
	    int len = ca.length;
	    StringBuilder jg = new StringBuilder((len + 1) * 26);
	    for (int i = 0; i < 26; i++){
	      for (int j = 0; j < len; j++) {
	        if (isUppercase(ca[j])) {
	          if (ca[j] == 'Z') {
	            ca[j] = 'A';
	          }
	          else
	          {
	            int tmp66_64 = j;
	            char[] tmp66_63 = ca; 
	            tmp66_63[tmp66_64] = ((char)(tmp66_63[tmp66_64] + '\001'));
	          }
	        } else if (isLowercase(ca[j])){
	          if (ca[j] == 'z') {
	            ca[j] = 'a';
	          }
	          else
	          {
	            int tmp106_104 = j;
	            char[] tmp106_103 = ca; 
	            tmp106_103[tmp106_104] = ((char)(tmp106_103[tmp106_104] + '\001'));
	          }
	        }
	    }
	      jg.append(ca);
	      jg.append('\n');
		    }
	    return jg.toString();
	  }
	public static String peigd(String input){//培根规律
			char ca[]=input.toCharArray();
			int pglen = ca.length;
			StringBuilder jg = new StringBuilder();
			for (int i =0;i<pglen;i++){
				if(isUppercase(ca[i])){
					ca[i]='A';
				jg.append(ca[i]);
			}else if(isLowercase(ca[i])){
				ca[i]='B';
				jg.append(ca[i]);
			}else{
			}
		}
		jg.append('\n');
	    return jg.toString();
	}
	public static String zjd(String input){//猪圈密码
		char ca [] = input.toCharArray();
		int zjl = ca.length;
		StringBuilder jg = new StringBuilder();
		for (int i=0;i<zjl;i++){
			switch(ca[i]){
			 case 'A':jg.append('J');
			 break;
			 case 'B':jg.append('K');
			 break;
			 case 'C':jg.append('L');
			 break;
			 case 'D':jg.append('M');
			 break;
			 case 'E':jg.append('N');
			 break;
			 case 'F':jg.append('O');
			 break;
			 case 'G':jg.append('P');
			 break;
			 case 'H':jg.append('Q');
			 break;
			 case 'I':jg.append('R');
			 break;
			 case 'J':jg.append('A');
			 break;
			 case 'K':jg.append('B');
			 break;
			 case 'L':jg.append('C');
			 break;
			 case 'M':jg.append('D');
			 break;
			 case 'N':jg.append('E');
			 break;
			 case 'O':jg.append('F');
			 break;
			 case 'P':jg.append('G');
			 break;
			 case 'Q':jg.append('H');
			 break;
			 case 'R':jg.append('I');
			 break;
			 case 'S':jg.append('W');
			 break;
			 case 'T':jg.append('X');
			 break;
			 case 'U':jg.append('Y');
			 break;
			 case 'V':jg.append('Z');
			 break;
			 case 'W':jg.append('S');
			 break;
			 case 'X':jg.append('T');
			 break;
			 case 'Y':jg.append('U');
			 break;
			 case 'Z':jg.append('V');
			 break;
			 case 'a':jg.append('j');
			 break;
			 case 'b':jg.append('k');
			 break;
			 case 'c':jg.append('l');
			 break;
			 case 'd':jg.append('m');
			 break;
			 case 'e':jg.append('n');
			 break;
			 case 'f':jg.append('o');
			 break;
			 case 'g':jg.append('p');
			 break;
			 case 'h':jg.append('q');
			 break;
			 case 'i':jg.append('r');
			 break;
			 case 'j':jg.append('a');
			 break;
			 case 'k':jg.append('b');
			 break;
			 case 'l':jg.append('c');
			 break;
			 case 'm':jg.append('d');
			 break;
			 case 'n':jg.append('e');
			 break;
			 case 'o':jg.append('f');
			 break;
			 case 'p':jg.append('g');
			 break;
			 case 'q':jg.append('h');
			 break;
			 case 'r':jg.append('i');
			 break;
			 case 's':jg.append('w');
			 break;
			 case 't':jg.append('x');
			 break;
			 case 'u':jg.append('y');
			 break;
			 case 'v':jg.append('z');
			 break;
			 case 'w':jg.append('s');
			 break;
			 case 'x':jg.append('t');
			 break;
			 case 'y':jg.append('u');
			 break;
			 case 'z':jg.append('v');
			 break;
			 default:
				 jg.append(ca[i]);
			}
		}
		jg.append('\n');
	    return jg.toString();
	    
	}
	public static String Rot13(String input){
	    StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {
	        char c = input.charAt(i);
	        if       (c >= 'a' && c <= 'm') c += 13;
	        else if  (c >= 'A' && c <= 'M') c += 13;
	        else if  (c >= 'n' && c <= 'z') c -= 13;
	        else if  (c >= 'N' && c <= 'Z') c -= 13;
	        jg.append(c);
	    }
	    return jg.toString();
	    
	}
	public static String Base64c(String input){//base64解密utf-8
		StringBuffer jg = new StringBuffer();
		String jiami = null;
		try{
			jiami = new String(new BASE64Decoder().decodeBuffer(input));
		}catch(IOException e){
			e.printStackTrace();
		}
		jg.append(jiami);
		return jg.toString();
		
	}
	public static String Base64j(String input){//base64加密utf-8
		StringBuffer jg = new StringBuffer();
		jg.append(new BASE64Encoder().encode(input.getBytes()));
		return jg.toString();
		
	}
	public static String Base64jg(String input){//base64加密gbk
		StringBuffer jg = new StringBuffer();
	    byte[] b = null;  
	    String s = null;  
	    try {  
	        b = input.getBytes("gbk");  
	    } catch (UnsupportedEncodingException e) {  
	        e.printStackTrace();  
	    }  
	    if (b != null) {  
	        s = new BASE64Encoder().encode(b);  
	    } 
	    jg.append(s);
		return jg.toString();
		
	}
	public static String Base64cg(String input){//base64解密gbk
		StringBuffer jg = new StringBuffer();
		String result = null;
		byte[] b = null;
	    if (input != null) {  
	        BASE64Decoder decoder = new BASE64Decoder();  
	        try {  
	            b = decoder.decodeBuffer(input);  
	            result = new String(b, "gbk");  
	        } catch (Exception e) {  
	            e.printStackTrace();  
	        }  
	    }  
	    jg.append(result);
		return jg.toString();
		
	}
	public static String Base32j(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b32e",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public static String Base32c(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b32d",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public static String Base16j(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b16e",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public static String Base16c(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\basecode.py");
	    PyFunction func = (PyFunction)interpreter.get("b16d",PyFunction.class);
	    PyObject rsadstr = func.__call__(new PyString(input));  
	    return (rsadstr.toString());
	}
	public static String peigen(String input){
	    PythonInterpreter interpreter = new PythonInterpreter();
		interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\OS\\peigen.py");
	    PyFunction func = (PyFunction)interpreter.get("run",PyFunction.class);
	    PyObject jg = func.__call__(new PyString(input));  
	    return jg.toString();
	}
	public static String MorseE(String input){//摩斯加密
		int len = input.length();
		StringBuffer jg = new StringBuffer(len *3);
		input = input.toLowerCase();
		for (int i = 0; i < len; i++)
	    {
	      char c = input.charAt(i);
	      if (isChar(c)) {
	        jg.append(morseCharacters[(c - 'a')]);
	        jg.append(" ");
	      }
	      else if (isDigit(c)) {
	        jg.append(morseDigits[(c - '0')]);
	        jg.append(" ");
	      }
	
	    }
		return jg.toString();
		
	}
	public static String MorseD(String input){//摩斯解码
	  initMorseTable();
	  String morse = format(input);
	  StringTokenizer st = new StringTokenizer(morse);
	  StringBuilder jg = new StringBuilder(morse.length() / 2);
	  while (st.hasMoreTokens())
	  {
	    jg.append(htMorse.get(st.nextToken()));
	  }
	  return jg.toString();
	  
	}
	public static String UrlEncoder(String input) throws UnsupportedEncodingException{//Url编码
		StringBuilder jg = new StringBuilder();
		String jm;
		jm = URLEncoder.encode(input,"utf-8");
		jg.append(jm);
		return jg.toString();
		
	}
	public static String UrlDecoder(String input) throws UnsupportedEncodingException{
		StringBuilder jg = new StringBuilder();
		String jm;
		jm = URLDecoder.decode(input,"utf-8");
		jg.append(jm);
		return jg.toString();
	}
	public static String UnicodeStre(String input){
		StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {	 
	        // 取出每一个字符
	        char c = input.charAt(i);
	        // 转换为unicode
	        jg.append("\\u" + Integer.toHexString(c));
	    }
	    return jg.toString();
	    
	}
	public static String UnicodeStrd(String input){
		StringBuilder jg = new StringBuilder();
	    String[] hex = input.split("\\\\u");
	    for (int i = 1; i < hex.length; i++) {
	        // 转换出每一个代码点
	        int data = Integer.parseInt(hex[i], 16);
	        // 追加成string
	        jg.append((char) data);
	    }
	    return jg.toString();
	    
	}
	public static String asciiZUnicode(String input){
		StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {	 
	        // 取出每一个字符
	        char c = input.charAt(i);
	        // 转换为unicode
	        jg.append("&#" + (int)(c)+";");
	    }
	    return jg.toString();
	    
	}
	public static String UnicodeZascii(String input){
		StringBuilder jg = new StringBuilder();
		Pattern pattern = Pattern.compile("\\&\\#(\\d+)");
		Matcher m =pattern.matcher(input);
	    while (m.find()){  
	        jg.append((char)Integer.valueOf(m.group(1)).intValue());  
	    }
	    return jg.toString();
	    
	}
	static boolean isLowercase(char c) {//判断是否小写字母
		return (c >= 'a') && (c <= 'z');
	}
	static boolean isUppercase(char c) {//判断是否为大写字母
		return (c >= 'A') && (c <= 'Z');
	}
	static boolean isChar(char c){//判断是否为字母
		return (isLowercase(c)) || (isUppercase(c));
	}
	static boolean isDigit(char c){//判断是否为数字
		return (c >='0')&&(c <= '9');
	}
	static String format(String input){
	    char[] ca = input.toCharArray();
	    int len = ca.length;
	    StringBuilder back = new StringBuilder(len);
	    for (int i = 0; i < len; i++)
	    {
	      switch (ca[i]) {
	      case '\n':
	        ca[i] = ' ';
	      case ' ':
	      case '-':
	      case '.':
	        back.append(ca[i]);
	      }
	    }
	    return back.toString();
	  }
	static Hashtable<String, Character> htMorse = new Hashtable();
	public static char morseToChar(String morse)
	  {
	    return ((Character)htMorse.get(morse)).charValue();
	  }
	public static void initMorseTable()
	  {
		boolean isInited = false;
	    if (isInited) {
	      return;
	    }
	    for (int i = 0; i < 26; i++)
	      htMorse.put(morseCharacters[i], Character.valueOf((char)(65 + i)));
	    for (int i = 0; i < 10; i++) {
	      htMorse.put(morseDigits[i], Character.valueOf((char)(48 + i)));
	    }
	    isInited = true;
	    }
	  static final String[] morseCharacters = {//摩斯密码 字母
	    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", 
	    ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", 
	    ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.." };
	  static final String[] morseDigits = {//摩斯密码 数字
	    "-----", ".----", "..---", "...--", "....-", 
	    ".....", "-....", "--...", "---..", "----." };
}
