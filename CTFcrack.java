/* 米斯特安全团队 Www.Hi-OurLife.Com
 * 作者：A先森_林晨
 * Mail:admin@hi-ourlife.com
 * QQ：627437686
 */
import java.math.BigInteger;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Enumeration;
import java.util.Hashtable;
import java.util.StringTokenizer;
import java.util.regex.Pattern;
import java.net.URLDecoder;
import java.net.URLEncoder;
import java.io.*;
import sun.misc.BASE64Decoder;
import sun.misc.BASE64Encoder;
import java.awt.*;
import javax.swing.*;
import javax.swing.plaf.FontUIResource;
import java.util.regex.*;
//导入了Jython包 可调用python
import org.python.core.*;
import javax.script.*;  
import org.python.core.PyFunction;  
import org.python.core.PyInteger;  
import org.python.core.PyObject;  
import org.python.util.PythonInterpreter;  
public class CTFcrack{
	private static String zlstr[]= new String[1024];
	private static int a1 = 0;
	private static int cs1 = 0;
	private static Font Zt = new Font("楷体", Font.PLAIN, 15);//赋值一个字体
	//主窗口
	private JFrame jf = new JFrame("米斯特安全团队 CTF Crypto类破解工具 v1.1");
    private JLabel jl = new JLabel("=====填写所需检测的密码====");
	private JTextArea Shuru = new JTextArea();
	private JTextArea ShuChu = new JTextArea();
	private JScrollPane gShuChu = new JScrollPane(this.ShuChu);
	private JScrollPane gShuru = new JScrollPane(this.Shuru);
	private JLabel JieG = new JLabel("======结果======");
	private JLabel AD = new JLabel("米斯特安全团队网址:www.hi-ourlife.com          程序作者:米斯特_A先森");
	private JMenuBar Menu = new JMenuBar();
    private JMenu zifu = new JMenu(" 解码方式");
	private JMenuItem caesar = new JMenuItem(" 凯撒密码>>解码");;
	private JMenuItem rot13 = new JMenuItem(" Rot13>>解码");
	private JMenuItem zhalan = new JMenuItem(" 栅栏密码>>解码");
	private JMenuItem peig = new JMenuItem(" 培根密码>>解码");
	private JMenuItem base64j = new JMenuItem(" 字符串>>Base64");
	private JMenuItem base64c = new JMenuItem(" Base64>>字符串");
	private JMenuItem morsee = new JMenuItem(" 字符串>>摩斯密码");
	private JMenuItem morsed = new JMenuItem(" 摩斯密码>>字符串");
	private JMenuItem UrlCoded = new JMenuItem(" Url编码>>字符串");
	private JMenuItem UrlCodee = new JMenuItem(" 字符串>>Url编码");
	private JMenuItem UnicoderStre = new JMenuItem(" 字符串>>Unicode");
	private JMenuItem UnicoderStrd = new JMenuItem(" Unicode>>字符串");
	private JMenuItem asciiZUnicode = new JMenuItem(" Ascii>>Unicode");
	private JMenuItem UnicodeZascii = new JMenuItem(" Unicode>>Ascii");
    private JMenu jinz = new JMenu(" 进制转换");
    private JMenuItem j2z8 = new JMenuItem(" 二进制>>八进制");
    private JMenuItem j2z10 = new JMenuItem(" 二进制>>十进制");
    private JMenuItem j2z16 = new JMenuItem(" 二进制>>十六进制");
    private JMenuItem j8z2 = new JMenuItem(" 八进制>>二进制");
    private JMenuItem j8z10 = new JMenuItem(" 八进制>>十进制");
    private JMenuItem j8z16 = new JMenuItem(" 八进制>>十六进制");
    private JMenuItem j10z2 = new JMenuItem(" 十进制>>二进制");
    private JMenuItem j10z8 = new JMenuItem(" 十进制>>八进制");
    private JMenuItem j10z16 = new JMenuItem(" 十进制>>十六进制");
    private JMenuItem j16z2 = new JMenuItem(" 十六进制>>二进制");
    private JMenuItem j16z8 = new JMenuItem(" 十六进制>>八进制");
    private JMenuItem j16z10 = new JMenuItem(" 十六进制>>十进制");
    private JMenu chaj = new JMenu(" 插件");
    private JMenuItem Tj = new JMenuItem(" 添加插件");
    private JMenuItem rsa = new JMenuItem(" RSAtools");
    //private JMenuItem xir = new JMenuItem(" 希尔加密");
    private JMenuItem cs;
    //rsatools窗口
    private void CreateJFrame(){//主窗口
    Container container = jf.getContentPane();
    container.setLayout(null);
    Menu.add(zifu);
    zifu.add(caesar);
    zifu.add(rot13);
    zifu.add(zhalan);
    zifu.add(peig);
    zifu.add(base64j);
    zifu.add(base64c);
    zifu.add(morsee);
    zifu.add(morsed);
    zifu.add(UrlCoded);
    zifu.add(UrlCodee);
    zifu.add(UnicoderStre);
    zifu.add(UnicoderStrd);
    zifu.add(asciiZUnicode);
    zifu.add(UnicodeZascii);
    Menu.add(jinz);
    jinz.add(j2z8);
    jinz.add(j2z10);
    jinz.add(j2z16);
    jinz.add(j8z2);
    jinz.add(j8z10);
    jinz.add(j8z16);
    jinz.add(j10z2);
    jinz.add(j10z8);
    jinz.add(j10z16);
    jinz.add(j16z2);
    jinz.add(j16z8);
    jinz.add(j16z10);
    Menu.add(chaj);
    chaj.add(Tj);
    chaj.add(rsa);
    //chaj.add(xir);
    ShuChu.setText("集合栅栏 凯撒 摩斯 Base64 Url编码 Unicode等多种解码方式 \n工具支持Python插件\n手头上有Python解码程序请联系我谢谢\n联系方式:QQ627437686\n懂Java的朋友也请联系我，共同开发。");
    //设置Swing的属性
    jf.setVisible(true);
    //jf.setResizable(false);
    int width1 = 530;
    jf.setSize(550, 530);//窗口
    jf.setDefaultCloseOperation(3);
    jl.setBounds(3, 20, width1, 20);//第一个标签
    JieG.setBounds(3, 240, width1, 20);//结果标签
    gShuru.setBounds(3, 40, width1, 200);//输入框
    gShuChu.setBounds(3, 260, width1, 200);//输出框
    AD.setBounds(3, 460, width1, 20);//广告
    Menu.setBounds(0, 0, width1,20);//菜单
    container.add(this.jl);
    container.add(this.gShuru);
    container.add(this.gShuChu);
    container.add(this.JieG);
    container.add(this.AD);
    container.add(Menu,BorderLayout.NORTH);
    //监听按钮
    caesar.addActionListener(new ActionListener() {//当按下凯撒密码
        public void actionPerformed(ActionEvent evt) {
          try {
            CTFcrack.this.Caesar(evt);
          } catch (Exception e) {
            e.printStackTrace();
          }
        } } );
    peig.addActionListener(new ActionListener() {//当按下凯撒密码
        public void actionPerformed(ActionEvent evt) {
          try {
            CTFcrack.this.peigd(evt);
          } catch (Exception e) {
            e.printStackTrace();
          }
        } } );
    rot13.addActionListener(new ActionListener() {//当按下凯撒密码
        public void actionPerformed(ActionEvent evt) {
          try {
            CTFcrack.this.Rot13(evt);
          } catch (Exception e) {
            e.printStackTrace();
          }
        } } );
    zhalan.addActionListener(new ActionListener() {//当按下栅栏密码
        public void actionPerformed(ActionEvent evt) {
          try {
            CTFcrack.this.Zhalan(evt);
          } catch (Exception e) {
            e.printStackTrace();
          }
        } } );
    base64j.addActionListener(new ActionListener() {//当按下Base64加密时
        public void actionPerformed(ActionEvent evt) {
          try {
            CTFcrack.this.Base64j(evt);
          } catch (Exception e) {
            e.printStackTrace();
          }
        } } );
    base64c.addActionListener(new ActionListener() {//当按下Base64解码时
        public void actionPerformed(ActionEvent evt) {
          try {
            CTFcrack.this.Base64c(evt);
          } catch (Exception e) {
            e.printStackTrace();
          }
        } } );
    morsee.addActionListener(new ActionListener() {//当按下摩斯加密时
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.MorseE(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });
    morsed.addActionListener(new ActionListener() {//当按下摩斯解密时
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.MorseD(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });
    UrlCodee.addActionListener(new ActionListener(){//当按下Url编码
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.UrlEncoder(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });
    UrlCoded.addActionListener(new ActionListener(){//当按下Url编码解码
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.UrlDecoder(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });
    UnicoderStre.addActionListener(new ActionListener(){
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.UnicodeStre(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });
    UnicoderStrd.addActionListener(new ActionListener(){
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.UnicodeStrd(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });    
	j2z8.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toOctalString(Long.parseLong(Shuru.getText(), 2)));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j2z10.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.valueOf(Shuru.getText(),2).toString());
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j2z16.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toHexString(Long.parseLong(Shuru.getText(), 2)));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j8z2.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toBinaryString(Long.valueOf(Shuru.getText(),8)));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j8z10.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.valueOf(Shuru.getText(),8).toString());
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j8z16.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toHexString(Long.valueOf(Shuru.getText(),8)));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j10z2.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toBinaryString(Long.parseLong(Shuru.getText())));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j10z8.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toOctalString(Long.parseLong(Shuru.getText())));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j10z16.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toHexString(Long.parseLong(Shuru.getText())));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j16z2.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toBinaryString(Long.valueOf(Shuru.getText(),16)));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j16z8.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.toOctalString(Long.valueOf(Shuru.getText(),16)));
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	j16z10.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				ShuChu.setText(Long.valueOf(Shuru.getText(),16).toString());
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
    UnicodeZascii.addActionListener(new ActionListener(){
    	public void actionPerformed(ActionEvent evt){
    		try{
    			CTFcrack.this.UnicodeZascii(evt);
    		}catch(Exception e){
    			e.printStackTrace();
    		}
    	}
    });
	asciiZUnicode.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			try{
				CTFcrack.this.asciiZUnicode(evt);
			}catch(Exception e){
				e.printStackTrace();
			}
		}
	});
	Tj.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			cs = new JMenuItem(" 测试"+cs1);
			chaj.add(cs);
			cs1 = cs1 +1 ;
		}
	});
	rsa.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			new CTFcrack().rsatools();
		}
	});
/*	xir.addActionListener(new ActionListener(){
		public void actionPerformed(ActionEvent evt){
			new CTFcrack().xirtools();
		}
	});*/
    }
    private JFrame Rsatools = new JFrame("RsaTools--Python插件");
    private JTextArea rsap = new JTextArea();
    private JTextArea rsaq = new JTextArea();
    private JTextArea rsae = new JTextArea();
    private JTextArea rsad = new JTextArea();
    private JLabel Rlabelp = new JLabel("p:");
    private JLabel Rlabelq = new JLabel("q:");
    private JLabel Rlabele = new JLabel("e:");
    private JLabel Rlabeld = new JLabel("d:");
    private JButton rsady = new JButton("Calc.D");
    private void rsatools(){//rsatools窗口
        Container container = Rsatools.getContentPane();
        container.setLayout(null);
        Rsatools.setVisible(true);
        Rsatools.setResizable(false);
        Rsatools.setSize(300, 200);//窗口
        Rsatools.setDefaultCloseOperation(WindowConstants.DISPOSE_ON_CLOSE);
        rsap.setBounds(30, 10, 200,20);
        rsaq.setBounds(30, 40,200, 20);
        rsae.setBounds(30, 70, 200, 20);
        rsad.setBounds(30, 100, 200, 20);
        container.add(rsap);
        container.add(rsaq);
        container.add(rsae);
        container.add(rsad);
        Rlabelp.setBounds(5, 10, 30, 20);
        Rlabelq.setBounds(5, 40,30,20);
        Rlabele.setBounds(5, 70, 30, 20);
        Rlabeld.setBounds(5, 100, 30, 20);
        container.add(Rlabelp);
        container.add(Rlabelq);
        container.add(Rlabele);
        container.add(Rlabeld);
        rsady.setBounds(80, 130, 100, 20);
        container.add(rsady);
    	rsady.addActionListener(new ActionListener(){//调用rsatools
    		public void actionPerformed(ActionEvent evt){
             PythonInterpreter interpreter = new PythonInterpreter();
    		 interpreter.execfile(System.getProperty("user.dir")+"\\Plugin\\rsa.py");
    		 BigInteger rsapstr=new BigInteger(rsap.getText());
             BigInteger rsaqstr=new BigInteger(rsaq.getText());
             BigInteger rsaestr=new BigInteger(rsae.getText());
             PyFunction func = (PyFunction)interpreter.get("rsa",PyFunction.class);
             PyObject rsadstr = func.__call__(new PyLong(rsapstr), new PyLong(rsaqstr),new PyLong(rsaestr));  
             rsad.setText(rsadstr.toString());
    		}
    	});
    }
    //下面是统一全局字体
    private static void InitGlobalFont(Font font) {//设置全局统一字体
		  FontUIResource fontRes = new FontUIResource(font);  
		  for (Enumeration<Object> keys = UIManager.getDefaults().keys();  
		  keys.hasMoreElements(); ) {  
		  Object key = keys.nextElement();  
		  Object value = UIManager.get(key);  
		  if (value instanceof FontUIResource) {  
		  UIManager.put(key, fontRes);  
		 }
	  }
	}  
	public static void main(String[] args){//主方法
	 System.out.println("完成");
	 InitGlobalFont(Zt);//赋值字体
	 new CTFcrack().CreateJFrame();
	}
	public void Zhalan(ActionEvent evt){//栅栏解码
		String Shuru = this.Shuru.getText();
		StringBuffer jg = new StringBuffer();
		 int x[] = new int[1024];
		 int sl = Shuru.length();
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
					 zlstr[a1]=(Shuru.substring((0+(x[i]*j)), (x[i]+(x[i]*j))));
					 a1 = a1+1;
				 }
				 int slen = zlstr[0].length();
				 for(int ji = 0;ji<slen;ji++){
					 for(int s=0;s<a1;s++){
						 jg.append(zlstr[s].substring(ji, ji+1));
					 }
				 }
				 a1 = 0;
				 jg.append("\n");
			 }
		 }else{
			 jg.append("解码失败...\n");
			 jg.append("尝试去除字符串中的空格解码\n");
			 sl = Shuru.replace(" ", "").length();
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
						 zlstr[a1]=(Shuru.substring((0+(x[i]*j)), (x[i]+(x[i]*j))));
						 a1 = a1+1;
					 }
					 int slen = zlstr[0].length();
					 for(int ji = 0;ji<slen;ji++){
						 for(int s=0;s<a1;s++){
							 jg.append(zlstr[s].substring(ji, ji+1));
						 }
					 }
					 a1 = 0;
					 jg.append("\n");
				 }
		 }
	   }
	 ShuChu.setText(jg.toString());
	 jg.delete(0, jg.length());
	 }
	public void Caesar(ActionEvent evt){//凯撒密码
		String input = Shuru.getText();
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
	    ShuChu.setText(jg.toString());
	    jg.delete(0,jg.length());
  }
	public void peigd(ActionEvent evt){
		String input = Shuru.getText();
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
	    ShuChu.setText(jg.toString());
	    jg.delete(0,jg.length());
	}
	public void Rot13(ActionEvent evt){
		String input = Shuru.getText();
        StringBuilder jg = new StringBuilder();
        for (int i = 0; i < input.length(); i++) {
            char c = input.charAt(i);
            if       (c >= 'a' && c <= 'm') c += 13;
            else if  (c >= 'A' && c <= 'M') c += 13;
            else if  (c >= 'n' && c <= 'z') c -= 13;
            else if  (c >= 'N' && c <= 'Z') c -= 13;
            jg.append(c);
        }
	    ShuChu.setText(jg.toString());
	    jg.delete(0,jg.length());
	}
	public void Base64c(ActionEvent evt){//base64解密
		String shuru = Shuru.getText();
		StringBuffer jg = new StringBuffer();
		String jiami = null;
		try{
			jiami = new String(new BASE64Decoder().decodeBuffer(shuru));
		}catch(IOException e){
			e.printStackTrace();
		}
		jg.append(jiami);
		ShuChu.setText(jg.toString());
		jg.delete(0, jg.length());
	}
	public void Base64j(ActionEvent evt){//base64加密
		String shuru = Shuru.getText();
		StringBuffer jg = new StringBuffer();
		jg.append(new BASE64Encoder().encode(shuru.getBytes()));
		ShuChu.setText(jg.toString());
		jg.delete(0, jg.length());
	}
	public void MorseE(ActionEvent evt){//摩斯加密
		String shuru = Shuru.getText();
		int len = shuru.length();
		StringBuffer jg = new StringBuffer(len *3);
		shuru = shuru.toLowerCase();
		for (int i = 0; i < len; i++)
	    {
	      char c = shuru.charAt(i);
	      if (isChar(c)) {
	        jg.append(morseCharacters[(c - 'a')]);
	        jg.append(" ");
	      }
	      else if (isDigit(c)) {
	        jg.append(morseDigits[(c - '0')]);
	        jg.append(" ");
	      }

	    }
		ShuChu.setText(jg.toString());
		jg.delete(0, jg.length());
	}
	public void MorseD(ActionEvent evt){//摩斯解码
	  initMorseTable();
	  String input = Shuru.getText();
	  String morse = format(input);
	  StringTokenizer st = new StringTokenizer(morse);
	  StringBuilder jg = new StringBuilder(morse.length() / 2);
	  while (st.hasMoreTokens())
	  {
	    jg.append(htMorse.get(st.nextToken()));
	  }
	  ShuChu.setText(jg.toString());
	  jg.delete(0, jg.length());
	}
	public void UrlEncoder(ActionEvent evt) throws UnsupportedEncodingException{//Url编码
		String input = Shuru.getText();
		StringBuilder jg = new StringBuilder();
		String jm;
		jm = URLEncoder.encode(input,"utf-8");
		jg.append(jm);
		ShuChu.setText(jg.toString());
		jg.delete(0, jg.length());
	}
	public void UrlDecoder(ActionEvent evt) throws UnsupportedEncodingException{
		String input = Shuru.getText();
		StringBuilder jg = new StringBuilder();
		String jm;
		jm = URLDecoder.decode(input,"utf-8");
		jg.append(jm);
		ShuChu.setText(jg.toString());
		jg.delete(0, jg.length());
	}
	public void UnicodeStre(ActionEvent evt){
		String input = Shuru.getText();
		StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {	 
	        // 取出每一个字符
	        char c = input.charAt(i);
	        // 转换为unicode
	        jg.append("\\u" + Integer.toHexString(c));
	    }
	    ShuChu.setText(jg.toString());
	    jg.delete(0, jg.length());
	}
	public void UnicodeStrd(ActionEvent evt){
		String input = Shuru.getText();
		StringBuilder jg = new StringBuilder();
	    String[] hex = input.split("\\\\u");
	    for (int i = 1; i < hex.length; i++) {
	        // 转换出每一个代码点
	        int data = Integer.parseInt(hex[i], 16);
	        // 追加成string
	        jg.append((char) data);
	    }
	    ShuChu.setText(jg.toString());
	    jg.delete(0, jg.length());
	}
	public void asciiZUnicode(ActionEvent evt){
		String input = Shuru.getText();
		StringBuilder jg = new StringBuilder();
	    for (int i = 0; i < input.length(); i++) {	 
	        // 取出每一个字符
	        char c = input.charAt(i);
	        // 转换为unicode
	        jg.append("&#" + (int)(c)+";");
	    }
	    ShuChu.setText(jg.toString());
	    jg.delete(0, jg.length());
	}
	public void UnicodeZascii(ActionEvent evt){
		String input = Shuru.getText();
		StringBuilder jg = new StringBuilder();
		Pattern pattern = Pattern.compile("\\&\\#(\\d+)");
		Matcher m =pattern.matcher(input);
        while (m.find()){  
            jg.append((char)Integer.valueOf(m.group(1)).intValue());  
        }
	    ShuChu.setText(jg.toString());
	    jg.delete(0, jg.length());
	}
	private boolean isLowercase(char c) {//判断是否小写字母
		return (c >= 'a') && (c <= 'z');
	}
	private boolean isUppercase(char c) {//判断是否为大写字母
		return (c >= 'A') && (c <= 'Z');
	}
	private  boolean isChar(char c){//判断是否为字母
		return (isLowercase(c)) || (isUppercase(c));
	}
	private boolean isDigit(char c){//判断是否为数字
		return (c >='0')&&(c <= '9');
	}
	//正则
	private String format(String input){
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
	private static Hashtable<String, Character> htMorse = new Hashtable();
	public char morseToChar(String morse)
	  {
	    return ((Character)htMorse.get(morse)).charValue();
	  }
	public static void initMorseTable()
	  {
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
	  private static boolean isInited = false;
	  private static final String[] morseCharacters = {//摩斯密码 字母
	    ".-", "-...", "-.-.", "-..", ".", "..-.", "--.", "....", "..", 
	    ".---", "-.-", ".-..", "--", "-.", "---", ".--.", "--.-", 
	    ".-.", "...", "-", "..-", "...-", ".--", "-..-", "-.--", "--.." };
	  private static final String[] morseDigits = {//摩斯密码 数字
	    "-----", ".----", "..---", "...--", "....-", 
	    ".....", "-....", "--...", "---..", "----." };
}
